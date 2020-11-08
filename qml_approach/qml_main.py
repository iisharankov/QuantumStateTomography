from __future__ import division
import multiprocessing as mp
import numpy as np
import random
from qiskit import *
from qiskit.quantum_info import random_statevector
import copt


random.seed(1)   # setting random seed to 1 for reproducibility
random_seed = 1  # setting the random seed inside the statevector


def generate_random_psi(num_qbits=2, debug=False):
    """
    Initialize our target state |psi>
    :param num_qbits: int, number of qbits
    :param debug: bool, will print |psi>
    :return: qiskit.quantum_info Statevector object
    """

    dim = 2**num_qbits
    psi = random_statevector(dim, seed=random_seed)
    if debug:
        print(psi)

    return psi


def initialize_theta(circ_depth=10, num_qbits=2):
    """
    Initialize the theta parameter vector
    :param circ_depth: int, number of parameterized layers in circuit
    :param num_qbits: int, number of qbits
    :return: np.array, values of theta
    """

    theta = np.zeros((circ_depth, num_qbits))
    return theta


def multi_processing_attempt(file_name):
    """
    file contains a list of quantum states (psi). This is a method for learning
    the parameterization vectors (theta) for an array of quantum states (psi)
    using multi-processing. The results (theta) are written to
    a new text file named (file_name + '_newTheta.txt'). An associated file
    named (file_name + '_newPsi.txt') which contains the states (psi) so
    that the 1st parameterization theta corresponds to the first state psi.

    :param file_name: str, name of file containing list of states psi
    :return: none
    """

    file = open(file_name, 'r')
    psi_lst = file.readlines()
    file.close()

    new_psi = file_name.split('.')[0] + '_newPsi.txt'
    new_theta = file_name.split('.')[0] + '_newTheta.txt'
    with open(new_psi, 'w') as P, open(new_theta, 'w') as T:
        p = mp.Pool(mp.cpu_count())
        print(f"Multiprocessing Pool created! Running with all {mp.cpu_count()} of your cores")

        for i, entry in enumerate(p.map(pool_function, psi_lst), 1):
            print('\rdone {0:%}'.format(i / len(psi_lst)))
            line, row = entry
            P.write(line)
            T.write(row)

    return


def pool_function(line, circ_depth, num_qbits):
    """
    Reads in the quantum state (psi) and runs the QML method to
    determine the associated parameterization (theta). returns
    a list containing the [psi, theta] written as strings.

    :param line: str, the quantum state psi, written as a str
    :param circ_depth: int, representing depth of VQC
    :param num_qbits: int, num qbits for state psi
    :return: list of len 2, containing the str psi (quantum state) and str theta (parameterization)
    """

    psi_vect = [complex(v) for v in line.split(',')]
    psi = qiskit.quantum_info.Statevector(psi_vect)

    initial_theta = initialize_theta(circ_depth=circ_depth, num_qbits=num_qbits)
    results, optimizer_data = copt.optimize_theta_scp(initial_theta, psi)  # Learn theta using VQCs
    optimized_theta = optimizer_data[-1]  # Final result

    theta_str_lst = [str(i) for i in optimized_theta]
    row = ",".join(theta_str_lst) + "\n"

    return [line, row]


def main():
    return


if __name__ == '__main__':
    main()
