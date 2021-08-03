import numpy as np
import matplotlib.pyplot as plt


# The neural network class
class NeuralNetwork:

    # The initializer function
    def __init__(self, inputs, outputs):
        self.inputs = inputs    # The training data sets
        self.outputs = outputs  # The training data correct answers
        self.weights = np.array([[.50], [.50], [.50], [.50], [.50]])    # The array of hidden neuron input weight values 
        self.error_history = [] # The array for storing error history over iterations while training
        self.epoch_list = []    # The array for holding data about each training epoch


    # A function for applying the sigmoid operator
    def sigmoid(self, x, deriv=False):
        if deriv == True:   # Option for if the input is a derivative value 
            return x * (1 - x)  # Operation for sigmoid derivative
        return 1 / (1 + np.exp(-x)) # Operation for sigmoid function


    # A function for feeding data forwards through the network's neurons
    def feed_forward(self):
        self.hidden = self.sigmoid(np.dot(self.inputs, self.weights))   # Applies the sigmoid function to the dot product of the input and weight vectors for each neruon 


    # A function to do back propagation on the network in order to adjust the neuron weights for training
    def backpropagation(self):
        self.error = self.outputs - self.hidden # Calculate the training error between the proper output and the network output
        delta = self.error * self.sigmoid(self.hidden, deriv=True)  # Compute the apropriate adjustments for each of the weights given the trining error 
        self.weights += np.dot(self.inputs.T, delta)    # Apply the computed adjustments to the neuron input weights 


    # The function to train the network on the training data for the specified ammount of epochs
    def train(self, epochs=25000):
        for epoch in range(epochs): # Iterate for the ammount of training epochs
            self.feed_forward() # Feed the training inputs forward through the network to get an ouput
            self.backpropagation()  #  Apply back propagation to the network given the output to compute and correct neuron error
            self.error_history.append(np.average(np.abs(self.error)))   # Append the error for the current training epoch to the error history array 
            self.epoch_list.append(epoch)   # Append the current epoch number to the epoch list


    # The function to take an input and apply the network to it to compute and return an output
    def predict(self, new_input):
        prediction = self.sigmoid(np.dot(new_input, self.weights))  # Applies the sigmoid function to the dot product of the input and weight vectors for each neruon 
        return round(prediction.item(0)) # Return the output from the network rounded to the nearest integer



inputs = np.array([[1, 1, 0, 0, 1],
                   [0, 0, 1, 1, 0],
                   [1, 1, 1, 0, 1],
                   [0, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1],
                   [1, 0, 1, 0, 1],
                   [0, 1, 0, 1, 0],
                   [1, 0, 1, 1, 1],
                   [0, 1, 1, 0, 0]])    # The training data input sets 

outputs = np.array([[1], [0], [1], [0], [0], [1], [1], [0], [1], [0]])  # The correct outputs for the training data sets

NN = NeuralNetwork(inputs, outputs) # Create a neural network object passing in the sets of training data inputs and outputs
NN.train()  # Train the network on the given training data
                           
example = np.array([[1, 1, 0, 1, 0]])   # Create an input to run the neural network on
example_output = 1  # The expected output for the first example input

example_2 = np.array([[0, 1, 0, 1, 0]]) # Create another example to run the network on
example_output_2 = 0   # The expected output for the second example input
                           
print('Prediction: ', NN.predict(example), '      Actual: ', example_output)     # Use the network to predict an output for the first example input and print it's reaturned prediction along with the expected actual output   
print('Prediction: ', NN.predict(example_2), '      Actual: ', example_output_2) # Use the network to predict an output for the second example input and print it's reaturned prediction along with the expected actual output

plt.figure(figsize=(15,5))  # Create a graph figure to plot the error over training
plt.plot(NN.epoch_list, NN.error_history)   # Plot the error history for each training epoch
plt.xlabel('Epoch') # Label the x axis as epoch number
plt.ylabel('Error') # Lbael the y axis as error magnitude
#plt.show()  # Plot the error graph