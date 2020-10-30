from __future__ import division
import sys


# Main file for QML
from qiskit import *
from qiskit.quantum_info import random_statevector
import numpy as np
import random
import qpu
import copt
import time

import multiprocessing as mp
import os
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
    # theta = np.random.uniform(0, 2*np.pi, (circ_depth, num_qbits))
    theta = np.zeros((circ_depth, num_qbits))
    return theta

def multi_processing_attempt():
    depth = 17
    qbits = 5
    file_name = "output_w_100.txt"
    file = open(file_name, 'r')
    psi_lst = file.readlines()
    file.close()

    newPsi = file_name.split('.')[0] + '_newPsi.txt'
    newTheta = file_name.split('.')[0] + '_newTheta.txt'
    with open(newPsi, 'w') as P, open(newTheta, 'w') as T:
        p = mp.Pool(mp.cpu_count())
        print(f"Multiprocessing Pool created! Running with all {mp.cpu_count()} of your cores")

        for i, entry in enumerate(p.map(poolThing, psi_lst), 1):
            print('\rdone {0:%}'.format(i / len(psi_lst)))
            line, row = entry
            P.write(line)
            T.write(row)

        # Without output
        # MS = p.map(poolThing, psi_lst)
        # for entry in MS:
        #     line, row = entry
        #     P.write(line)
        #     T.write(row)

def poolThing(line):
    depth = 8
    qbits = 3

    psi_vect = [complex(v) for v in line.split(',')]
    psi = qiskit.quantum_info.Statevector(psi_vect)
    initial_theta = initialize_theta(circ_depth=depth, num_qbits=qbits)
    results, optimizer_data = copt.optimize_theta_scp(initial_theta, psi)  # Final result
    optimized_theta = optimizer_data[-1]

    theta_str_lst = [str(i) for i in optimized_theta]
    row = ",".join(theta_str_lst) + "\n"

    return [line, row]

def main():
    start = time.time()
    multi_processing_attempt()
    print("that took ", time.time() - start, " seconds")
    # file_lst = ["testing_data_3qbit_psi.txt", "training_data_3qbit_psi.txt", "validation_data_3qbit_psi.txt"]
    # depth = 8
    # qbits = 3
    #
    # for file_name in file_lst:
    #     print('running file: {}'.format(file_name))
    #     new_name = file_name.split('.')[0] + '_theta.txt'
    #     file = open(file_name, 'r')
    #     psi_lst = file.readlines()
    #     new_file = open(new_name, 'w')
    #
    #     for index, line in enumerate(psi_lst):
    #         print('processing line #: {}'.format(index))
    #         psi_vect = [complex(v) for v in line.split(',')]
    #         psi = qiskit.quantum_info.Statevector(psi_vect)
    #         initial_theta = initialize_theta(circ_depth=depth, num_qbits=qbits)
    #         results, optimizer_data = copt.optimize_theta_scp(initial_theta, psi)  # Final result
    #         optimized_theta = optimizer_data[-1]
    #
    #         theta_str_lst = [str(i) for i in optimized_theta]
    #         print(theta_str_lst)
    #         row = "{}".format(theta_str_lst[0])
    #         for char in theta_str_lst[1:]:
    #             row += ',' + char
    #
    #         row += '\n'
    #         print(row)
    #         final_str = ",".join(theta_str_lst)
    #         print(final_str)
    #         new_file.write(row)
    #
    #     file.close()
    #     new_file.close()

    return


if __name__ == '__main__':
    main()
