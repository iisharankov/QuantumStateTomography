import numpy as np
import tensorflow as tf
import tensorflow.keras
from qiskit import *
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
        tf.keras.layers.Dense(50, activation='relu', input_shape=theta_raw.shape),
        tf.keras.layers.Dense(50, activation='softmax'),
        tf.keras.layers.Dense(40, activation='relu'),
        tf.keras.layers.Dense(40, activation='softmax'),
        tf.keras.layers.Dense(25, activation='relu'),
        tf.keras.layers.Dense(16, activation='softmax'),
        tf.keras.layers.Dense(8, activation='sigmoid')
        # tf.keras.layers.Dense(16, activation='softsign')
    ])
    # model.summary()



    model.compile(optimizer='adam', loss=my_loss_fn)
    model.fit(epochs=500, batch_size=5000, x=xTrain, y=yTrain)

    # Save the model for future use
    model.save(f'{modelname}.h5')  # creates a HDF5 file

def main():
    # Load data
    # psi_raw, theta_raw = open_files("training/training_data_3qbit_psi.txt", "training/training_data_3qbit_psi_theta.txt")
    psi_raw, theta_raw = open_files("output_w_10k_newPsi.txt", "output_w_10k_newTheta.txt")

    # Create the different datasets
    (xTrain, yTrain), (xValidate, yValidate), (xTest, yTest) = splitData(theta_raw, psi_raw)
    modelname = "QML_Model_700"
    train_model(xTrain, yTrain, theta_raw, modelname)
    model = load_model(f'{modelname}.h5', custom_objects={'my_loss_fn': my_loss_fn})
    model.evaluate(x=xValidate, y=yValidate)

    pred = model.predict(xTest)

    x = []
    for i, j in zip(pred, yTest):
        x.append([round(np.abs(a-b), 4) for a, b in zip(i, j)])

    a = np.array(x)
    print(np.mean(a, axis=0))


if __name__ == "__main__":
    main()
