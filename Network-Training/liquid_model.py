import tensorflow as tf
from tensorflow import keras


class LiquidOdeCell(keras.layers.Layer):
    def __init__(self, units=32, **kwargs):
        super(LiquidOdeCell, self).__init__(**kwargs)
        self.units = units
        self.state_size = units

    def build(self, input_shape):
        # Define the weights for the recurrent cell
        self.kernel = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer='glorot_uniform',
            name='kernel'
        )
        self.recurrent_kernel = self.add_weight(
            shape=(self.units, self.units),
            initializer='orthogonal',
            name='recurrent_kernel'
        )
        self.bias = self.add_weight(
            shape=(self.units,),
            initializer='zeros',
            name='bias'
        )

    def call(self, inputs, states):
        prev_output = states[0]

        # Define the dynamics of the ODE
        def ode_fn(y, inputs):
            return tf.matmul(inputs, self.kernel) + tf.matmul(y, self.recurrent_kernel) + self.bias

        # Integrate using a simple Euler method
        dt = 0.1  # Time step for the Euler integration
        output = prev_output + dt * ode_fn(prev_output, inputs)

        return output, [output]  # Return the output and the new state


# Define LiquidRNN model
class LiquidRNNModel(keras.Model):
    def __init__(self, units=32, output_size=3, **kwargs):
        super(LiquidRNNModel, self).__init__(**kwargs)
        self.rnn = keras.layers.RNN(LiquidOdeCell(units))
        self.dense1 = keras.layers.Dense(units, activation='tanh')
        self.dense2 = keras.layers.Dense(output_size, activation='softmax')

    def call(self, inputs):
        x = self.rnn(inputs)
        x = self.dense1(x)
        return self.dense2(x)
