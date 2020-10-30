import numpy as np
import tensorflow as tf
import tensorflow.keras
from qiskit import *


def main():
    psi_data = open("training/training_data_3qbit_psi.txt", 'r')
    lines_psi = psi_data.readlines()
    psi_raw = np.zeros((len(lines_psi), 8), dtype=np.complex)

    for i, line in enumerate(lines_psi):
        psi_raw[i] = [complex(j) for j in line.split(',')]

    psi_raw = np.real(psi_raw)
    psi_data.close()

    theta_data = open("training/training_data_3qbit_psi_theta.txt", 'r')
    lines_theta = theta_data.readlines()
    theta_raw = np.zeros((len(lines_theta), 24))

    for i, line in enumerate(lines_theta):
        theta_raw[i] = [float(j) for j in line.split(',')]

    theta_data.close()

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(50, activation='relu', input_shape=theta_raw.shape),
        tf.keras.layers.Dense(8, activation='sigmoid')
    ])

    model.summary()

    def my_loss_fn(y_true, y_pred):
        squared_difference = tf.square(y_true - y_pred)
        return tf.reduce_mean(squared_difference, axis=-1)

    model.compile(optimizer='adam', loss=my_loss_fn)

    # tf.trainable_variables()
    history = model.fit(epochs=100, x=theta_raw, y=psi_raw)

    psi_data = open("validation/validation_data_3qbit_psi.txt", 'r')
    lines_psi = psi_data.readlines()
    psi_raw_val = np.zeros((len(lines_psi), 8), dtype=np.complex)

    for i, line in enumerate(lines_psi):
        psi_raw_val[i] = [complex(j) for j in line.split(',')]

    psi_raw_val = np.real(psi_raw_val)
    psi_data.close()

    theta_data = open("validation/validation_data_3qbit_psi_theta.txt", 'r')
    lines_theta = theta_data.readlines()
    theta_raw_val = np.zeros((len(lines_theta), 24))

    for i, line in enumerate(lines_theta):
        theta_raw_val[i] = [float(j) for j in line.split(',')]

    theta_data.close()

    model.evaluate(x=theta_raw_val, y=psi_raw_val)

    return


if __name__ == "__main__":
    main()
