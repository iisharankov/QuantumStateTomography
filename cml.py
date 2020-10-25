import numpy as np

from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD
import keras.backend as K
from keras.utils.generic_utils import get_custom_objects

from qiskit.quantum_info import state_fidelity

def load_generated_data_to_text(xfilename='XData', yfilename='YData'):
    X = []
    Y = []

    with open(xfilename + '.txt', 'r') as a, open(yfilename + '.txt', 'r') as b:
        xLines, yLines = a.readlines(), b.readlines()

        for curX, curY in zip(xLines, yLines):
            # Remove whitespace + last comma, then split on comma
            test1 = curX.rstrip()[:-1].split(",")
            test2 = curY.rstrip()[:-1].split(",")

            # convert each element to a float and map+append it
            X.append(list(map(float, test1)))
            Y.append(list(map(float, test2)))

    return X, Y

def splitData(x_data, y_data, pTrain=70, pValidate=20, pTest=10):

    assert len(x_data) == len(y_data)

    if pTrain + pValidate + pTest != 100:
        print('WARNING: pTrain, pValidate, pTest must add up to 100%')
        return ([], []), ([], []), ([], [])

    else:
        b1 = int(np.floor(len(x_data) * (pTrain/100)))
        b2 = int(np.ceil(len(
            x_data) * ((100-pTest)/100)))

        xTrain, yTrain = x_data[:b1], y_data[:b1]
        xValidate, yValidate = x_data[b1: b2], y_data[b1: b2]
        xTest, yTest = x_data[b2:], y_data[b2:]

        return (xTrain, yTrain), (xValidate, yValidate), (xTest, yTest)

def convertBackToImg(stateVec):
    """
    Given a list of even length, with float/ints, convert
    list to complex assuming a +ib, a+ib, a+ib, ... form
    :param stateVec: list of floats
    :return: list of complex
    """
    assert len(stateVec) % 2 == 0  # Make sure the list is even
    outputList = []

    while len(stateVec) > 1:  # While the list is not empty

        # pop two elements, convert to complex and append
        temp, stateVec = stateVec[:2], stateVec[2:]
        outputList.append(complex(temp[0], temp[1]))

    return outputList

def custom_loss(actsvect, estsvect):
    '''
    consumes numpy array of the ML's estimates and the actual
    returns loss function 1-sqrt(fidelity)
    '''
    #We gotta turn the arrays into a list of a+ib first
    estlst = convertBackToImg(estsvect.tolist()[0])
    actslst = convertBackToImg(actsvect.tolist()[0])

    fidelity = state_fidelity(estlst, actslst)

    return 1-K.sqrt(fidelity)

def trainModel(modelName, xTrain, yTrain):

    def QMSoftMax(x):
        '''
        consumes a list  of scores x, returns qsoftmax
        '''
        softmax = K.exp(x) / K.sum(K.exp(x), axis=1, keepdims=True)
        a = K.sqrt(softmax)
        arctan = K.cos(x)/K.sin(x)
        # b = K.exp(np.multiply(1j, arctan))
        # return np.multiply(a, b)

        # b = K.exp(1j * arctan)
        b = K.sin(arctan) + (1j * K.cos(arctan))
        return a * b


    get_custom_objects().update({'QMSoftMax': Activation(QMSoftMax)})

    # def custom_loss(y_true, y_pred):
    #     return K.mean(K.square(K.abs(y_pred - y_true)))

    # The ML Model
    model = Sequential()
    model.add(Dense(12))
    model.add(Dense(12))
    model.add(Dense(8))
    # model.add(Activation('sigmoid'))
    model.add(Activation(QMSoftMax, name='QMSoftMax'))



    sgd = SGD(lr=0.5)
    model.compile(loss=custom_loss, optimizer=sgd)
    model.fit(xTrain, yTrain, verbose=1,  batch_size=1, epochs=250)

    model.save(f'{modelName}.h5')  # creates a HDF5 file 'my_model.h5'

def outputModel(model, xTrain, yTrain):
    print(model.predict(xTrain)[0])
    print(yTrain[0])
    print(model.predict(xTrain)[1])
    print(yTrain[1])
    # print("\n DIFFERENCE \n")
    # inn = np.abs(yTrain - model.predict(xTrain))
    # output = [np.round(i, 5) for i in inn]
    # print(inn[0:4])

def testModel(model, xTest, yTest):

    predict = model.predict(xTest)
    print(np.mean(np.square(predict - yTest)))  # discrepancy  between prediction and what we expect
    score = model.evaluate(xTest, yTest, verbose=0)
    print("Test score is:", score)

if __name__ == '__main__':
    modelName = 'my_model_middleLayerof12_customActivation'

    # Extract the datasets and separate them into separate groups
    X, Y = load_generated_data_to_text()
    (xTrain, yTrain), (xValidate, yValidate), (xTest, yTest) = splitData(X, Y)

    convertBackToImg(Y[1])
    # trainModel(modelName, xTrain, yTrain)
    model = load_model(f'{modelName}.h5')
    # outputModel(model, xTrain, yTrain)
    testModel(model, xTest, yTest)



