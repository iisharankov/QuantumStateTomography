import numpy as np
import tensorflow as tf
import tensorflow.keras
from qiskit import *

from keras.optimizers import SGD
from keras.models import Sequential, load_model
from keras.utils.generic_utils import get_custom_objects

def splitData(x_data, y_data, pTrain=70, pValidate=20, pTest=10):

    assert len(x_data) == len(y_data)

    if pTrain + pValidate + pTest != 100:
        print('WARNING: pTrain, pValidate, pTest must add up to 100%')
        return ([], []), ([], []), ([], [])

    else:
        b1 = int(np.floor(len(x_data) * (pTrain/100)))
        b2 = int(np.ceil(len(x_data) * ((100-pTest)/100)))

        xTrain, yTrain = x_data[:b1], y_data[:b1]
        xValidate, yValidate = x_data[b1: b2], y_data[b1: b2]
        xTest, yTest = x_data[b2:], y_data[b2:]

        return (xTrain, yTrain), (xValidate, yValidate), (xTest, yTest)

def open_files(psi_file, theta_file):
    with open(psi_file, 'r') as psi_data:
        lines_psi = psi_data.readlines()

        psi_raw = np.zeros((len(lines_psi), 8), dtype=np.complex)

        for i, line in enumerate(lines_psi):
            psi_raw[i] = [complex(j) for j in line.split(',')]
        psi_raw = np.real(psi_raw)

    with open(theta_file, 'r') as theta_data:
        lines_theta = theta_data.readlines()
        theta_raw = np.zeros((len(lines_theta), 24))

        for i, line in enumerate(lines_theta):
            theta_raw[i] = [float(j) for j in line.split(',')]

    return psi_raw, theta_raw

def open_files_w_complex(psi_file, theta_file):
    with open(psi_file, 'r') as psi_data:
    # psi_data = open("complex_psi_newPsi.txt", 'r')
        lines_psi = psi_data.readlines()
        psi_raw = np.zeros((len(lines_psi), 8*2))

        for i, line in enumerate(lines_psi):
            val = [complex(j) for j in line.split(',')]
            vect = []
            for num in val:
                vect.append(np.real(num))
                vect.append(np.imag(num))

            psi_raw[i] = vect

    with open(theta_file, 'r') as theta_data:
        lines_theta = theta_data.readlines()
        theta_raw = np.zeros((len(lines_theta), 24))
        for i, line in enumerate(lines_theta):
            theta_raw[i] = [float(j) for j in line.split(',')]

    return psi_raw, theta_raw


def my_loss_fn(y_true, y_pred):
    squared_difference = tf.square(y_true - y_pred)
    return tf.reduce_mean(squared_difference, axis=-1)

def train_model(xTrain, yTrain, theta_raw, modelname):
    # Train model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(50, activation='softmax', input_shape=theta_raw.shape),
        tf.keras.layers.Dense(50, activation='relu'),
        tf.keras.layers.Dense(40, activation='softmax'),
        tf.keras.layers.Dense(40, activation='softmax'),
        tf.keras.layers.Dense(25, activation='relu'),
        tf.keras.layers.Dense(16, activation='softmax'),
        tf.keras.layers.Dense(16, activation='softsign')
    ])
    # model.summary()



    sgd = SGD(lr=0.075)

    # model.compile(optimizer='adam', loss=my_loss_fn)
    model.compile(optimizer=sgd, loss=my_loss_fn)
    model.fit(epochs=2500, batch_size=2500, x=xTrain, y=yTrain)

    # Save the model for future use
    # model.save(f'{modelname}.h5')  # creates a HDF5 file

def main():
    # Load data
    psi_raw, theta_raw = open_files_w_complex("3Qbit_complex_psi_1k_newPsi.txt", "3Qbit_complex_psi_1k_Theta.txt")
    # psi_raw, theta_raw = open_files_w_complex("complex_w_100_newPsi.txt", "complex_w_100_newTheta.txt")

    # Create the different datasets
    (xTrain, yTrain), (xValidate, yValidate), (xTest, yTest) = splitData(theta_raw, psi_raw)

    modelname = "QML_Model_700"
    # train_model(xTrain, yTrain, theta_raw, modelname)
    model = load_model(f'{modelname}.h5', custom_objects={'my_loss_fn': my_loss_fn})
    model.evaluate(x=xValidate, y=yValidate)

    pred = model.predict(xTest)k

    x = []
    fidelity = []
    for i, j in zip(pred, yTest):
        x.append([round(np.abs(a-b), 4) for a, b in zip(i, j)])
        # fidelity.append([1 - np.sqrt(a * b) for a, b in zip(i, j)])

    complexFidelity = []
    for tempX, tempY in zip(pred, yTest):
        a = tempX
        b = tempY
k
        tempTerm1, tempTerm2 = 0, 0
        while len(a) > 0:
            tempTerm1 += (a[0] * b[0]) + (a[1] * b[1])
            tempTerm2 += (a[0] * b[1]) - (a[1] * b[0])
            a = a[2:]
            b = b[2:]

        complexFidelity.append(pow(tempTerm1, 2) + pow(tempTerm2, 2))


    # Take the averagek
    print("Average error in test dataset for all {len(x)} complex coefficients")
    print(np.mean(np.array(x), axis=0))
    # print(np.mean(np.array(fidelity), axis=0))
    print("Average fidelity over all the training set: ", np.mean(np.array(complexFidelity), axis=0))


if __name__ == "__main__":
    main()
