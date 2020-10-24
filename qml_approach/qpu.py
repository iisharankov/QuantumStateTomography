from qiskit import *
import numpy as np
circ_depth = 12  # sets the circuit depth of the variational quantum circuit


# def ansatz_from_paper():
#     return


def construct_variational_circ(ansatz, theta, num_qbits=5):
    var_circ = qiskit.QuantumCircuit(num_qbits)

    for layer in range(circ_depth - 1):
        for qbit in range(num_qbits):

            if layer % 2 == 1:  # odd layer

    return

