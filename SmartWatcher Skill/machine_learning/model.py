from keras.models import Sequential
from keras.layers import Dense
import numpy as np
# fix random seed for reproducibility
# np.random.seed(7)

dataset = np.loadtxt("Uptime_Lengths.csv", delimiter="	")
# split into input (X) and output (Y) variables
X = dataset[:,0]
Y = dataset[:,1]

# create model
model = Sequential()
model.add(Dense(12, input_dim=1, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.summary()

# Compile model
model.compile(loss='mean_squared_logarithmic_error', optimizer='Nadam', metrics=['accuracy'])

# Fit the model
model.fit(X, Y, epochs=200000, batch_size=10)

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
