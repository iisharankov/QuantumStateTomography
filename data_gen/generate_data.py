# Main file for generating data
from qiskit import *
import numpy as np
import random


def random_state_gen(alpha=np.pi/2):
    """
    Produces a quantum state vector given alpha

    :param alpha: float, angle between (0, 2pi)
    :return: statevect: an array of complex #s
    :return: circ: a qiskit.QuantumCircuit object
    """
    circ = qiskit.QuantumCircuit(2)  # initialize a quantum circuit with 2 qbits

    circ.rx(alpha, 0)
    circ.cx(0, 1)                  # create a 'kind of' entanglement between them

    backend = qiskit.Aer.get_backend('statevector_simulator')  # get simulator
    job = execute(circ, backend)
    result = job.result()
    statevect = result.get_statevector(circ)  # state_vector as expressed in Z_basis

    return statevect, circ


def change_basis(circ, basis):
    """
    Changes the basis that the state vector is expressed in

    :param circ: qiskit.QuantumCircuit object
    :param basis: float, 'x' for x basis, 'y' for y basis, anything else for z basis
    :return: statevect: an array of floats
    """

    circ_copy = circ.copy()

    if basis == 'x':
        circ_copy.ry(-np.pi / 2, (0, 1))  # change basis to x

    elif basis == 'y':
        circ_copy.rx(np.pi / 2, (0, 1))  # change basis to y

    backend = qiskit.Aer.get_backend('statevector_simulator')  # get simulator
    job = execute(circ_copy, backend)
    result = job.result()
    statevect = result.get_statevector(circ_copy)  # state_vector

    return statevect


def measure(state_vect, shots=1_000_000):
    """
    Make measurements along the z basis

    :param state_vect: an array of floats
    :param shots: int representing # of measurements
    :return: dictionary with measured state and frequency of measurements
    """
    states = ['00', '01', '10', '11']
    prob_vect = state_vect * np.conj(state_vect)
    prob_vect = [float(i) for i in prob_vect]
    # print(prob_vect)
    measurements = np.random.multinomial(shots, prob_vect)

    results = []
    for state, frequency in zip(states, measurements):
        # results[state] = frequency/shots
        results.append(frequency/shots)

    return results

def combineMatrix(xDict, yDict, zDict):
    xList = []
    for x,y,z in zip(xDict, yDict, zDict):
        xList.extend((x, y, z))

    return xList

def main():
    X = []
    Y = []
    n = 5
    for i in range(n):
        #  generated state vector in z and the associated circuit
        psi, circ = random_state_gen(random.random()*4)

        results_z = measure(psi)
        results_x = measure(change_basis(circ, 'x'))
        results_y = measure(change_basis(circ, 'y'))

        temp = []
        for i in psi:
            temp.extend([i.real, i.imag])
        Y.append(temp)
        X.append(combineMatrix(results_x, results_y, results_z))


    print(X)
    print(Y)


if __name__ == '__main__':
    main()
