# Main file for QML
from qiskit import *
from qiskit.quantum_info import random_statevector
import numpy as np
import qpu
import random

random.seed(1)  # setting random seed to 1 for reproducibility
random_seed = 1


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


def initialize_theta(num_qbits=2):
    """
    Initialize the theta parameter vector
    :param num_qbits: int, number of qbits
    :return: np.array, values of theta
    """
    theta = np.random.uniform(0, 2*np.pi, (qpu.circ_depth, num_qbits))
    return theta


def main():
    # psi = generate_random_psi(2, debug=True)
    # theta = initialize_theta()
    # pprint(theta)
    return


if __name__ == '__main__':
    main()
