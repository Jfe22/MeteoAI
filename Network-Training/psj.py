"""
This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs (CC BY-NC-ND 4.0) License
and is subject to patent application regulations.

Filename: psj.py
Author: João da Silva Pereira (joao.pereira@ipleiria.pt)
Description: This module implements the PSJ method.
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# Define the model prediction function
def predict_with_model(model, image):
    return model.predict(image.reshape(1, 100, 100, 4), verbose=0)


# function that implements the PSJ method for the 1st Deep Learning layer (João Silva Pereira)
def PSJmethod(model, N_neuronio, Xinput, Youtput, x_train, y_train):
    z = np.zeros((N_neuronio, Xinput * 4))  # reshaping here
    for i in range(0, N_neuronio):
        if i < Youtput:
            soma = np.zeros([100, 100, 4])
            cont = 0
            for n in range(0, len(x_train)):
                if y_train[n] == np.mod(i, Youtput):
                    soma += x_train[n]
                    cont += 1
            soma /= cont

            # Call the prediction function inside the loop
            soma_r = predict_with_model(model, soma)

            if i == 2:
                # print(soma.shape)
                print(soma)
                # Plot the array as an image
                plt.imshow(soma)
                plt.axis('off')  # Disable axis
                plt.show()

                print(soma_r.shape)
                # print(soma)
                # Plot the array as an image
                plt.imshow(soma_r.reshape(200, 200))
                plt.axis('off')  # Disable axis
                plt.show()

            soma = tf.reshape(soma_r, [100 * 100 * 4])  # reshaping here
            s = np.array(soma, dtype=np.complex128)  # 64-bit complex numbers (higher precision)
            s = np.fft.fft(s)
            s = np.cos(np.angle(s)) + np.sin(np.angle(s)) * 1j
            s = np.fft.ifft(s)
            z[i] = s.real
        else:
            z[i] = z[np.mod(i, Youtput)]
    return z


# function that implements the PSJ method for the other Deep Learning layers (João Silva Pereira)
def iniL2(N_neur, inp):
    LastLayerANN = np.zeros((N_neur, inp))
    for r in range(0, N_neur):
        if np.mod(r, inp) == 0:
            for k in range(0, inp):
                for s in range(0, inp):
                    if k == s:
                        if (r + k) < N_neur:
                            LastLayerANN[r + k][s] = 1
    return LastLayerANN

