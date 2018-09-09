from keras.models import Sequential
from keras.layers import Dense
import numpy
# fix random seed for reproducibility
# numpy.random.seed(7)

# load pima indians dataset
dataset = numpy.loadtxt("noMoreHeadaches_dummy.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:34]
Y = dataset[:,35:39]

# create model
model = Sequential()
model.add(Dense(12, input_dim=34, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(4, activation='sigmoid'))

model.summary()

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X, Y, epochs=20, batch_size=10)

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# predict_dataset = numpy.loadtxt("noMoreHeadachesPredict.csv", delimiter=",")
# print(predict_dataset.shape)
# predict_X = predict_dataset[0:34]
# print(predict_X.shape)
#
# prediction = model.predict(predict_X, 34, 0)

# numpy.savetxt("noMoreHeadachesPredicted.csv", prediction, delimiter=",")
