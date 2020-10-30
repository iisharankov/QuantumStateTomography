import numpy as np

from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD
import keras.backend as K
import keras.utils as U
from keras.layers import Layer, LSTM, Embedding, LeakyReLU
from keras.utils.generic_utils import get_custom_objects

from qiskit.quantum_info import state_fidelity


# Custom layer
class MyCustomLayer(Layer):
    def __init__(self, output_dim,  **kwargs):
        super().__init__(**kwargs) ##
        self.output_dim = output_dim
        super(MyCustomLayer, self).__init__(**kwargs)
    def build(self, input_shape):
        self.kernel = self.add_weight(name = 'kernel', shape = (input_shape[1], self.output_dim),
                                      initializer = 'normal', trainable = True)
        super(MyCustomLayer, self).build(input_shape) # Be sure to call this at the end

    def call(self, input_data):
        return K.dot(input_data, self.kernel)

    def compute_output_shape(self, input_shape):
        return (input_shape[0] * 1j, self.output_dim)

    def get_config(self):
        config = super().get_config().copy()
        config.update({'output_dim': self.output_dim,})
        return config


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
        # Convert to complex and append
        outputList.append(complex(stateVec[0], stateVec[1]))
        stateVec = stateVec[2:]

    return outputList

def custom_loss(actsvect, estsvect):
    '''
    consumes numpy array of the ML's estimates and the actual
    returns loss function 1-sqrt(fidelity)
    '''
    #We gotta turn the arrays into a list of a+ib first
    # sess = K.get_session()
    # estlst = convertBackToImg(estsvect.tolist()[0])
    # actslst = convertBackToImg(actsvect.tolist()[0])
    # print(K.eval(estsvect))
    # print(type(K.eval(estsvect)))
    # if tf.is_tensor(estsvect):

    # if tf.is_tensor(estsvect):
    #     # t = estsvect.eval(session=tf.compat.v1.Session())
    #     t = estsvect.eval(session=sess)
    #     # t = estsvect.asarray()
    #
    # estlst = convertBackToImg(tf.make_ndarray(estsvect))
    # actslst = convertBackToImg(tf.make_ndarray(actsvect))

    # fidelity = state_fidelity(estlst, actslst)

    x = actsvect
    xo = estsvect
    # return ((1 + x) / 2 * K.log(xo)) + ((1 - x) / 2 * K.log(1 - xo))
    return (1/2) * ((1 - xo) * K.log(1 - K.tanh(x)) + (1 + xo) * K.log(1+K.tanh(x)))
    # fidelity = K.pow(K.abs(K.dot(actsvect, K.transpose(estsvect))), 2)
    # return 1-K.sqrt(fidelity)

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
        # b = K.sin(arctan) + (1j * K.cos(arctan))
        return a * K.cos(arctan)  # a * b

    # def QMSoftMax(x):
    #     softmax = K.exp(x) / K.sum(K.exp(x), axis=1, keepdims=True)
    #     a = K.sqrt(softmax)
    #     phase =  K.cos(x)/K.sin(x)
    #     # phase = np.pi*K.softsign(x) #another possibility for phase
    #
    #     real_part = a * K.cos(phase)
    #     imaginary_part = a * K.sin(phase)
    #
    #     # return (K.sigmoid(x) * 5) - 1
    #     # return real_part
    #     return (real_part, imaginary_part)


    # def custom_loss(y_true, y_pred):
    #     return K.mean(K.square(K.abs(y_pred - y_true)))
    get_custom_objects().update({'QMSoftMax': Activation(QMSoftMax)})

    # The ML Model
    model = Sequential()
    model.add(Dense(12))
    model.add(Dense(12))
    model.add(Dense(8))
    model.add(MyCustomLayer(8))
    # model.add(Activation('sigmoid'))
    model.add(Activation(QMSoftMax, name='QMSoftMax'))

    # for 100 - score is: 0.21507123112678528
    # for 250 - Test score is: 0.48923787474632263

    sgd = SGD(lr=0.5)
    model.compile(loss=custom_loss, optimizer=sgd)
    # model.compile(loss='mean_squared_error', optimizer=sgd)

    model.fit(xTrain, yTrain, verbose=2, batch_size=1, epochs=25)
    model.save(f'{modelName}.h5')  # creates a HDF5 file 'my_model.h5'
    return model

def outputModel(model, xTrain, yTrain):
    for i in range(5):
        print(f"#{i}: Pred", model.predict(xTrain)[i])
        print(f"#{i}: True", yTrain[i])
    # print("\n DIFFERENCE \n")
    #     inn = np.abs(yTrain - model.predict(xTrain))
    #     output = [np.round(i, 5) for i in inn]
    #     print(inn[0:4])

def modelTest(model, xTest, yTest):

    predict = model.predict(xTest)
    # print(np.mean(np.square(predict - yTest)))  # discrepancy between prediction and what we expect
    score = model.evaluate(xTest, yTest, verbose=0)
    print("Test score is:", score)

def trainDoubleModel(modelName, xTrain, yTrain):

    # The ML Model
    model = Sequential()
    model.add(Dense(12))
    # model.add(Dense(12))
    # model.add(Embedding(input_dim=12, output_dim=8))
    # model.add(LSTM(units=8))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    # model.add(LeakyReLU(alpha=0.1))
    # model.add(Activation('softsign'))
    # model.add(Activation(SoftMax, name='SoftMax'))
    model.add(Dense(8))

    sgd = SGD(lr=0.5)
    # model.compile(loss=custom_loss, optimizer=sgd)
    model.compile(loss='mean_squared_error', optimizer=sgd)
    #
    model.fit(xTrain, yTrain, verbose=2, batch_size=1, epochs=100)
    return model

def listDoubler(myList):
    """
    Given a list of lists of floats, return a list of list of floats
    where the sublists are 2 times larger, and all negative values are seperates
    [-5, 0, 3] -> [0, 5, 0, 0, 3, 0]
    :param myList: list of list of floats
    :return: list of list of floats
    """
    output = []
    j = 0
    for subList in myList:
        output.append([])
        for i in subList:
            if i > 0:
                output[j].append(i)
                output[j].append(0.0)
            else:
                output[j].append(0.0)
                output[j].append(abs(i))
        j += 1

    return output




if __name__ == '__main__':
    modelName = 'myFirstModel'



    # Extract the datasets and separate them into separate groups
    X, Y = load_generated_data_to_text()
    (xTrain, yTrain), (xValidate, yValidate), (xTest, yTest) = splitData(X, Y)

    print(xTrain)
    print(yTrain)
    yTrainReal = listDoubler([[j[0], j[2], j[4], j[6]] for j in yTrain])
    yTrainImag = listDoubler([[j[1], j[3], j[5], j[7]] for j in yTrain])

    modelReal = trainDoubleModel(modelName, xTrain, yTrainReal)
    modelImag = trainDoubleModel(modelName, xTrain, yTrainImag)
    modelReal.save(f'{modelName}_Real.h5')  # creates a HDF5 file 'my_model.h5'
    modelImag.save(f'{modelName}_Imag.h5')  # creates a HDF5 file 'my_model.h5'

    # model = load_model(f'{modelName}.h5', custom_objects={'custom_loss':custom_loss, 'MyCustomLayer':MyCustomLayer})
    # modelReal = load_model(f'{modelName}_Real.h5', custom_objects={'custom_loss': custom_loss,})
    # modelImag = load_model(f'{modelName}_Imag.h5', custom_objects={'custom_loss': custom_loss,})
    modelReal = load_model(f'{modelName}_Real.h5')
    modelImag = load_model(f'{modelName}_Imag.h5')
    print("we")
    outputModel(modelReal, xTrain, yTrainReal)
    print('--------')
    outputModel(modelReal, xTrain, yTrainImag)

    yTestReal = listDoubler([[j[0], j[2], j[4], j[6]] for j in yTest])
    yTestImag = listDoubler([[j[1], j[3], j[5], j[7]] for j in yTest])
    modelTest(modelReal, xTest, yTestReal)
    modelTest(modelImag, xTest, yTestImag)



