import numpy as np

from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD
import keras.backend as K
from keras.utils.generic_utils import get_custom_objects

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
        b2 = int(np.ceil(len(x_data) * ((100-pTest)/100)))

        xTrain, yTrain = x_data[:b1], y_data[:b1]
        xValidate, yValidate = x_data[b1: b2], y_data[b1: b2]
        xTest, yTest = x_data[b2:], y_data[b2:]

        return (xTrain, yTrain), (xValidate, yValidate), (xTest, yTest)


def trainModel(modelName, xTrain, yTrain):

    def QMSoftMax(x):
        '''
        consumes a list  of scores x, returns qsoftmax
        '''
        softmax = K.exp(x) / K.sum(K.exp(x), axis=1, keepdims=True)
        a = K.sqrt(softmax)
        tan = K.cos(x)/K.sin(x)
        # b = K.exp(np.multiply(1j, tan))
        # return np.multiply(a, b)

        b = K.exp(1j * tan)
        # b = K.sin(tan) + (1j * K.cos(tan))
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
    model.compile(loss='mean_squared_error', optimizer=sgd)
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


    trainModel(modelName, xTrain, yTrain)
    model = load_model(f'{modelName}.h5')
    # outputModel(model, xTrain, yTrain)
    testModel(model, xTest, yTest)



