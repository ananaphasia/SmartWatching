# -*- coding: utf-8 -*-

# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License"). You may not use this file except in
# compliance with the License. A copy of the License is located at
#
#    http://aws.amazon.com/asl/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import boto3
import json
from alexa.skills.smarthome import AlexaResponse

import time
import random

aws_dynamodb = boto3.client('dynamodb')


def lambda_handler(request, context):

    # Dump the request for logging - check the CloudWatch logs
    print('lambda_handler request  -----')
    print(json.dumps(request))

    if context is not None:
        print('lambda_handler context  -----')
        print(context)

    # Validate we have an Alexa directive
    if 'directive' not in request:
        aer = AlexaResponse(
            name='ErrorResponse',
            payload={'type': 'INVALID_DIRECTIVE',
                     'message': 'Missing key: directive, Is the request a valid Alexa Directive?'})
        return send_response(aer.get())

    # Check the payload version
    payload_version = request['directive']['header']['payloadVersion']
    if payload_version != '3':
        aer = AlexaResponse(
            name='ErrorResponse',
            payload={'type': 'INTERNAL_ERROR',
                     'message': 'This skill only supports Smart Home API version 3'})
        return send_response(aer.get())

    # Crack open the request and see what is being requested
    name = request['directive']['header']['name']
    namespace = request['directive']['header']['namespace']

    # Handle the incoming request from Alexa based on the namespace

    if namespace == 'Alexa.Authorization':
        if name == 'AcceptGrant':
            # Note: This sample accepts any grant request
            # In your implementation you would use the code and token to get and store access tokens
            grant_code = request['directive']['payload']['grant']['code']
            grantee_token = request['directive']['payload']['grantee']['token']
            aar = AlexaResponse(namespace='Alexa.Authorization', name='AcceptGrant.Response')
            return send_response(aar.get())

    if namespace == 'Alexa.Discovery':
        if name == 'Discover':
            adr = AlexaResponse(namespace='Alexa.Discovery', name='Discover.Response')
            capability_alexa = adr.create_payload_endpoint_capability()
            capability_alexa_powercontroller = adr.create_payload_endpoint_capability(
                interface='Alexa.PowerController',
                supported=[{'name': 'powerState'}])
            adr.add_payload_endpoint(
                friendly_name='Sample Switch',
                endpoint_id='sample-switch-01',
                capabilities=[capability_alexa, capability_alexa_powercontroller])
            return send_response(adr.get())

    if namespace == 'Alexa.PowerController':
        # Note: This sample always returns a success response for either a request to TurnOff or TurnOn
        endpoint_id = request['directive']['endpoint']['endpointId']
        power_state_value = 'OFF' if name == 'TurnOff' else 'ON'
        correlation_token = request['directive']['header']['correlationToken']

        # Check for an error when setting the state
        state_set = set_device_state(endpoint_id=endpoint_id, state='powerState', value=power_state_value)
        if not state_set:
            return AlexaResponse(
                name='ErrorResponse',
                payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()

        # Check for an error when setting TurnOn/TurnOff time
        if power_state_value == 'ON':
            TurnOn_set = set_device_time(endpoint_id=endpoint_id, state='TurnOnTime', value=get_seconds_timestamp())
            if not TurnOn_set:
                return AlexaResponse(
                    name='ErrorResponse',
                    payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()
            global turned_on
            turned_on = get_seconds_timestamp()
            time.sleep(random.uniform(1.500,2.500))
            TurnOff_set = set_device_state(endpoint_id=endpoint_id, state='powerState', value='OFF')
            print("turnedoff")
            # if not TurnOff_set:
            #     return AlexaResponse(
            #         name='ErrorResponse',
            #         payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()
        if power_state_value == 'OFF':
            TurnOff_set = set_device_time(endpoint_id=endpoint_id, state='TurnOffTime', value=get_seconds_timestamp())
            if not TurnOff_set:
                return AlexaResponse(
                    name='ErrorResponse',
                    payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()
            global turned_off
            turned_off = get_seconds_timestamp()
            uptime_length = get_uptime_length(turned_on, turned_off)
            last_uptime_length = set_device_time(endpoint_id=endpoint_id, state='LastUptimeLength', value=uptime_length)
            if not last_uptime_length:
                return AlexaResponse(
                    name='ErrorResponse',
                    payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()
            add_value_to_file(uptime_length)

        apcr = AlexaResponse(correlation_token=correlation_token)
        apcr.add_context_property(namespace='Alexa.PowerController', name='powerState', value=power_state_value)
        return send_response(apcr.get())


def send_response(response):
    # TODO Validate the response
    print('lambda_handler response -----')
    print(json.dumps(response))
    return response


def set_device_state(endpoint_id, state, value):
    attribute_key = state + 'Value'
    response = aws_dynamodb.update_item(
        TableName='SampleSmartHome',
        Key={'ItemId': {'S': endpoint_id}},
        AttributeUpdates={attribute_key: {'Action': 'PUT', 'Value': {'S': value}}})
    print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

def set_device_time(endpoint_id, state, value):
    attribute_key = state
    value = str(value)
    response = aws_dynamodb.update_item(
        TableName='SampleSmartHome',
        Key={'ItemId': {'S': endpoint_id}},
        AttributeUpdates={attribute_key: {'Action': 'PUT', 'Value': {'S': value}}})
    print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

def get_uptime_length(turned_on, turned_off):
    uptime_length = turned_off - turned_on
    return uptime_length

def add_value_to_file(uptime_length):
    # TODO: Replace this with S3 integration
    # uptime_length = uptime_length.encode("utf-8")
    # csv_list = open('Uptime_Lengths.csv', 'w')
    # csv_list.write("{}\n".format(uptime_length))
    # csv_list.close()
    return True

def get_utc_timestamp(seconds=None):
    return time.strftime('%Y-%m-%dT%H:%M:%S.00Z', time.gmtime(seconds))

def get_seconds_timestamp():
    return time.time()
