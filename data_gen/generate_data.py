# Main file for generating data
from qiskit import *
import numpy as np
import random
import pickle


def random_state_gen(num_qbits, random_seed=1, real_valued_state=False):
    """
    Produces a quantum state vector given number of qbits

    :param num_qbits: int, number of qbits > 0
    :param random_seed: int, optional parameter to set 'randomness'
    :param real_valued_state: bool, if true, produce a very special type of psi
    :return: qiskit.quantum_info.Statevector object: an array of complex #s
    """
    dim = 2**num_qbits

    if real_valued_state:
        psi_vect = np.random.uniform(size=dim)
        norm = np.linalg.norm(psi_vect)
        psi_vect = psi_vect / norm
        psi = qiskit.quantum_info.Statevector(psi_vect)

    else:
        psi = qiskit.quantum_info.random_statevector(dim, seed=random_seed)

    return psi


def change_basis(psi, basis='z', random_seed=1):
    """
    Changes the basis that the state vector is expressed in return
    change of basis unitary

    :param psi: qiskit.quantum_info.Statevector object
    :param basis: float, 'x' for x basis, 'y' for y basis, anything else for z basis
    :param random_seed: int, the seed for the random unitary genertation
    :return: statevect: qiskit.quantum_info.Statevector object
    :return: unitary: a qiskit.quantum_info.Operator object
    """

    num_qbits = psi.num_qubits
    qbit_tuple = tuple(range(num_qbits))
    circ = qiskit.QuantumCircuit(num_qbits)

    if basis == 'z':
        circ.i(qbit_tuple)  # apply identity since all states are by default in z basis

    elif basis == 'x':
        circ.ry(-np.pi / 2, qbit_tuple)  # change basis to x

    elif basis == 'y':
        circ.rx(np.pi / 2, qbit_tuple)  # change basis to y

    else:  # generate random unitary to change basis
        unitary = qiskit.quantum_info.random_unitary(2**num_qbits, seed=random_seed)
        statevect = psi.evolve(unitary)
        return statevect, unitary     # this is broken ! DO NOT USE!

    statevect = psi.evolve(circ)  # state_vector
    unitary = qiskit.quantum_info.Operator(circ)

    return statevect, unitary


def measure(state_vect, shots=1_000_000, random_seed=1):
    """
    Make measurements along the z basis

    :param state_vect: qiskit.quantum_info.Statevector object
    :param shots: int, representing # of measurements
    :param random_seed: int, for setting the 'randomness'
    :return: list with measured state and frequency of measurements
    """

    state_vect.seed(random_seed)
    probability_vec = state_vect.probabilities()
    results = np.random.multinomial(shots, probability_vec)

    results = [i/shots for i in results]
    return results


def measure_raw(state_vect, shots=1_000_000, random_seed=1):
    """
    Make measurements along the z basis, return raw data

    :param state_vect: qiskit.quantum_info.Statevector object
    :param shots: int, representing # of measurements
    :param random_seed: int, for setting the 'randomness'
    :return: a list of np.arrays containing the measurement results shape = (shots, num_qbits)
    """

    state_vect.seed(random_seed)
    data_lst= state_vect.sample_memory(shots)
    results = []
    for measurement in data_lst:
        results.append([float(j) for j in list(measurement)])

    return results

def combineMatrix(xDict, yDict, zDict):
    xList = []
    for x,y,z in zip(xDict, yDict, zDict):
        xList.extend((x, y, z))

    return xList


def save_generated_data_to_text(X, Y, xfilename='XData', yfilename='YData'):
    # Save this generated data into individual text files, stripped of whitespace for easy parsing later
    with open("./" + xfilename + '.txt', 'w+') as a, open("./" + yfilename + '.txt', 'w+') as b:
        assert len(X) == len(Y)  # The length of X & Y should be the same

        # For each line in X, Y we want to save each element individually
        for x, y in zip(X, Y):
            for i in x:
                a.write(str(i) + ",")

            for i in y:
                b.write(str(i).replace("(", "").replace(")", "") + ",")

            # new line for each X,Y line
            a.write("\n")
            b.write("\n")


def main():
    # X = []
    # Y = []
    # n = 100
    # for i in range(n):
    #     # special_psi = random_state_gen(3, real_valued_state=True)
    #     psi = random_state_gen(5)
    #     psi_x = change_basis(psi, 'x')
    #     psi_y = change_basis(psi, 'y')
    #
    #     x_results = measure(psi_x, shots=100_000_000_000)
    #     y_results = measure(psi_y, shots=100_000_000_000)
    #     z_results = measure(psi, shots=100_000_000_000)
    #
    #     # print(x_results)
    #     Y.append(psi.data)
    #     X.append(combineMatrix(x_results, y_results, z_results))
    #
    # save_generated_data_to_text(X, Y)

    psi = random_state_gen(3)
    results = measure_raw(psi, shots=1_000)
    print(results)

    with open('../unsupervised_approach/data.pkl', 'wb') as f:
        pickle.dump(results, f)


if __name__ == '__main__':
    main()
