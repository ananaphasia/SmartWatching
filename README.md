## SmartWatching
AI Alexa Skill which automatically controls lights. Created at uncommonhacks 2019.

## Inspiration

What if your lights turned on and off by themselves? Without you spending a minute programming them? Enter SmartWatcher. Much more than turning the lights off at pre-specified times, SmartWatcher analyses user actions in order to turn lights on and off at the appropriate time of day. 

## What it does

SmartWatcher controls the lights in your home, without you lifting a finger. Through an analysis powered by artificial intelligence, SmartWatcher does high-level pattern recognition and pattern analytics, and then, after a certain amount of time, controls the lights in your home themselves.

## How I built it

SmartWatcher is built using Amazon Lambda, using a Python 3.6 backend and DynamoDB for record management. 

## Challenges I ran into

I did not have support for Amazon S3, so I had to devise a temporary way to store data locally and send it off to the neural networks as fast as possible. Also, the serverless architecture of Amazon Lambda wasn't the best for my use case of network training, so I had to do initial modeling on a separate server.

## Accomplishments that I'm proud of

The machine learning backend works, even though the models still need to be trained and optimized some more. 

## What I learned

I learned how to use Amazon Lambda architecture and DynamoDB. 

## What's next for SmartWatcher

SmartWatcher will eventually have the same capability for music, temperature regulation, and (maybe) self-driving!

[Website](http://localhost:1313/SmartWatching/), [GitHub](https://github.com/as4mo3/SmartWatching), and [presentation](https://docs.google.com/presentation/d/1hnEbS85fWeWY49ii0HkPnh7WHXjcbiytJyHt43siGMw/edit?usp=sharing) links.

---

Created at uncommonhacks 2019.

Image courtesy of [David Kaplan](https://geomarketing.com/voice-activated-connected-device-usage-jumps-130-percent-this-year).
