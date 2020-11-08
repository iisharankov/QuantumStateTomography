# Main file for generating data
from qiskit import *
import numpy as np


def random_state_gen(num_qbits, random_seed=1, real_valued_state=False):
    """
    Produces a quantum state vector given number of qbits

    :param num_qbits: int, number of qbits > 0
    :param random_seed: int, optional parameter to set 'randomness'
    :param real_valued_state: bool, if true, produce a psi with only real valued coefficients
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
    data_lst = state_vect.sample_memory(shots)
    results = []
    for measurement in data_lst:
        results.append([float(j) for j in list(measurement)])

    return results


def generate_psi_data_set(file_name, shots=1000, num_qbits=3):
    """
    Create a data set of radomly generated quantum states.
    Constructs a text file where each line corresponds to the quantum state.
    each comma seperated value is the complex coefficient to the basis states
    of an Nqbit state (basis states ordered from least to greatest left to right)

    :param file_name: str, file name (not including .txt)
    :param shots: int, number of randomly generated states
    :param num_qbits: int, number of qbits in quantum state
    :return: None
    """

    file = open(file_name + '.txt', 'w')

    for index in range(shots):
        psi = random_state_gen(num_qbits, real_valued_state=False)
        psi_data = [str(i) for i in psi.data]

        row = '{}'.format(psi_data[0])
        for i in psi_data[1:]:
            row += ',' + i

        row += '\n'
        file.write(row)

    file.close()
    return


def generate_raw_data_set(file_name, state_vect, shots=5000):
    """
    Generate a data set containing raw measurements for a quantum state.
    The first line in the text file is the quantum state, subsequent lines
    are the raw measurements obtained.

    :param file_name: str, name of text file
    :param state_vect: qiskit.QuantumCircuit object,
    :param shots: int, number of raw measurements
    :return: None
    """

    file = open(file_name + '.txt', 'w')

    state_vect_lst = [str(i) for i in state_vect.data]
    psi = "{}".format(state_vect_lst[0])
    for i in state_vect_lst[1:]:
        psi += ',' + i

    psi += '\n'
    file.write(psi)

    measurements = measure_raw(state_vect, shots)
    for x in measurements:
        x_str_lst = [str(j) for j in x]
        row = "{}".format(x_str_lst[0])

        for x_str in x_str_lst[1:]:
            row += ',' + x_str

        row += '\n'
        file.write(row)

    file.close()
    return


def main():
    generate_psi_data_set("3Qbit_complex,psi_1k")
    return


if __name__ == '__main__':
    main()
