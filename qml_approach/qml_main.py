# Main file for QML
from qiskit import *
from qiskit.quantum_info import random_statevector
import numpy as np
import random
import qpu
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
    theta = np.random.uniform(0, 2*np.pi, (circ_depth, num_qbits))
    return theta


def main():
    file_lst = ["testing_data_3qbit_psi.txt", "training_data_3qbit_psi.txt", "validation_data_3qbit_psi.txt"]
    depth = 8
    qbits = 3

    for file_name in file_lst:
        print('running file: {}'.format(file_name))
        new_name = file_name.split('.')[0] + '_theta.txt'
        file = open(file_name, 'r')
        psi_lst = file.readlines()
        new_file = open(new_name, 'w')

        for index, line in enumerate(psi_lst):
            print('processing line #: {}'.format(index))
            psi_vect = [complex(v) for v in line.split(',')]
            psi = qiskit.quantum_info.Statevector(psi_vect)
            initial_theta = initialize_theta(circ_depth=depth, num_qbits=qbits)
            results, optimizer_data = copt.optimize_theta_scp(initial_theta, psi)  # Final result
            optimized_theta = optimizer_data[-1]

            theta_str_lst = [str(i) for i in optimized_theta]
            row = "{}".format(theta_str_lst[0])
            for char in theta_str_lst[1:]:
                row += ',' + char

            row += '\n'
            new_file.write(row)

        file.close()
        new_file.close()

    return


if __name__ == '__main__':
    main()
