# Main file for generating data
from qiskit import *
import numpy as np


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
        psi = qiskit.quantum_info.Statevector(psi_vect)

    else:
        psi = qiskit.quantum_info.random_statevector(dim, seed=random_seed)

    return psi


def change_basis(psi, basis):
    """
    Changes the basis that the state vector is expressed in

    :param psi: qiskit.quantum_info.Statevector object
    :param basis: float, 'x' for x basis, 'y' for y basis, anything else for z basis
    :return: statevect: qiskit.quantum_info.Statevector object
    """

    num_qbits = psi.num_qubits
    circ = qiskit.QuantumCircuit(num_qbits)

    if basis == 'x':
        circ.ry(-np.pi / 2, (0, 1))  # change basis to x

    elif basis == 'y':
        circ.rx(np.pi / 2, (0, 1))  # change basis to y

    statevect = psi.evolve(circ)  # state_vector
    return statevect


def measure(state_vect, shots=1_000_000, random_seed=1):
    """
    Make measurements along the z basis

    :param state_vect: qiskit.quantum_info.Statevector object
    :param shots: int, representing # of measurements
    :param random_seed: int, for setting the 'randomness'
    :return: dictionary with measured state and frequency of measurements
    """
    state_vect.seed(random_seed)
    results = state_vect.sample_counts(shots)

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
                b.write(str(i) + ",")

            # new line for each X,Y line
            a.write("\n")
            b.write("\n")


def main():
    # X = []
    # Y = []
    # n = 100
    # for i in range(n):
    #     #  generated state vector in z and the associated circuit
    #     psi, circ = random_state_gen(random.random()*4)
    #
    #     results_z = measure(psi)
    #     results_x = measure(change_basis(circ, 'x'))
    #     results_y = measure(change_basis(circ, 'y'))
    #
    #     temp = []
    #     for i in psi:
    #         temp.extend([i.real, i.imag])
    #     Y.append(temp)
    #     X.append(combineMatrix(results_x, results_y, results_z))
    #
    # save_generated_data_to_text(X, Y)

    special_psi = random_state_gen(3, real_valued_state=True)
    psi = random_state_gen(3)
    psi_x = change_basis(psi, 'x')
    psi_y = change_basis(psi, 'y')

    x_results = measure(psi_x, shots=100)
    y_results = measure(psi_y, shots=100)
    z_results = measure(psi, shots=100)

    print("|psi> = {}".format(psi))
    print("|special_psi> = {}".format(special_psi))
    print("x_axis measurement results: {}".format(x_results))
    print("y_axis measurement results: {}".format(y_results))
    print("z_axis measurement results: {}".format(z_results))

    return


if __name__ == '__main__':
    main()
