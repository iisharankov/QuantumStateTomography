import numpy as np
import tensorflow as tf
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import load_model


def split_data(x_data, y_data, ptrain=0.70, pvalidate=0.20, ptest=0.10):
    """
    Given two arrays of equal size, split the data sets into
    training, validation and testing datasets of the specified size.

    :param x_data: np.array, first data set
    :param y_data: np.array, second data set
    :param ptrain: float, precent of total data_set to be allocated for training
    :param pvalidate: float, precent of total data_set to be allocated for validation
    :param ptest: float, precent of total data_set to be allocated for testing
    :return: 3 tuples (train), (validate), (test), each of size 2 (x_data, y_data)
    """

    assert len(x_data) == len(y_data)

    if not np.isclose(ptrain + pvalidate + ptest, 1.0):
        print('WARNING: ptrain, pvalidate, ptest must add up to 100%')
        return ([], []), ([], []), ([], [])

    else:
        b1 = int(np.floor(len(x_data) * ptrain))
        b2 = int(np.ceil(len(x_data) * (1-ptest)))

        xtrain, ytrain = x_data[:b1], y_data[:b1]
        xvalidate, yvalidate = x_data[b1: b2], y_data[b1: b2]
        xtest, ytest = x_data[b2:], y_data[b2:]

        return (xtrain, ytrain), (xvalidate, yvalidate), (xtest, ytest)


def open_files(psi_file, theta_file):
    """
    function to open the txt files and extract the meta data from
    the files containing the raw data for quantum states (psi) and the parameterizations (theta) .
    :param psi_file: str, path to the txt file containing quantum state data
    :param theta_file: str, path to the txt file containing the parameterization data
    :return: 2 np.arrays, containing the raw data: psi_data and theta_data
    """

    with open(psi_file, 'r') as psi_data:
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
    """
    custom loss func, implemented mean squared error in this case
    between y_true and y_pred

    :param y_true: np.array, vector containing "true" values
    :param y_pred: np.array, vector containing "predicted" values
    :return: float, mean squared error between the two vectors
    """

    squared_difference = tf.square(y_true - y_pred)
    return tf.reduce_mean(squared_difference, axis=-1)


def train_model(xtrain, ytrain, input_len, modelname):
    """
    Training a simple feed forward NN model to learn the
    mapping between variational circuit parameterizations and
    the associated quantum states

    :param xtrain: parameterization data set for training
    :param ytrain: associated quantum state data set for training
    :param input_len: int, number of components in the parameterization vector (len(xtrain[i]))
    :param modelname: str, name of the model
    :return: None
    """

    # Train model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(50, activation='softmax', input_shape=(None, input_len)),
        tf.keras.layers.Dense(50, activation='relu'),
        tf.keras.layers.Dense(40, activation='softmax'),
        tf.keras.layers.Dense(40, activation='softmax'),
        tf.keras.layers.Dense(25, activation='relu'),
        tf.keras.layers.Dense(16, activation='softmax'),
        tf.keras.layers.Dense(16, activation='softsign')
    ])
    # model.summary()

    sgd = SGD(lr=0.075)

    model.compile(optimizer=sgd, loss=my_loss_fn)
    # model.fit(epochs=2500, batch_size=2500, x=xtrain, y=ytrain)
    model.fit(epochs=5, batch_size=2500, x=xtrain, y=ytrain)

    # Save the model for future use
    model.save(f'{modelname}.h5')  # creates a HDF5 file
    return


def main():
    # Load data
    psi_raw, theta_raw = open_files("./data/3Qbit_complex_psi_1k_newPsi.txt",
                                    "./data/3Qbit_complex_psi_1k_newTheta.txt")

    # Create the different datasets
    (xTrain, yTrain), (xValidate, yValidate), (xTest, yTest) = split_data(theta_raw, psi_raw)

    modelname = "./model/QML_Model_700"
    # train_model(xTrain, yTrain, theta_raw.shape[1], modelname)  # train model
    model = load_model(f'{modelname}.h5', custom_objects={
                       'my_loss_fn': my_loss_fn})
    model.evaluate(x=xValidate, y=yValidate)

    pred = model.predict(xTest)

    x = []
    for i, j in zip(pred, yTest):
        x.append([round(np.abs(a-b), 4) for a, b in zip(i, j)])

    complex_fidelity = []
    for tempX, tempY in zip(pred, yTest):
        a = tempX
        b = tempY

        temp_term1, temp_term2 = 0, 0
        while len(a) > 0:
            temp_term1 += (a[0] * b[0]) + (a[1] * b[1])
            temp_term2 += (a[0] * b[1]) - (a[1] * b[0])
            a = a[2:]
            b = b[2:]

        complex_fidelity.append(pow(temp_term1, 2) + pow(temp_term2, 2))

    # Take the average and print results
    print("Average error in test dataset for all 8 complex coefficients (split into (real, im)):")
    print(np.mean(np.array(x), axis=0))
    print("Average fidelity over all the training set: ", np.mean(np.array(complex_fidelity), axis=0))
    return


if __name__ == "__main__":
    main()
