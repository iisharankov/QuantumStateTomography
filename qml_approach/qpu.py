from qiskit import *
import numpy as np
import qml_main
circ_depth = 6  # sets the circuit depth of the variational quantum circuit (d + 1 from paper)


# def ansatz_from_paper():
#     return


def construct_variational_circ(theta, num_qbits=5, debug=False):
    var_circ = qiskit.QuantumCircuit(num_qbits)
    lst_qbits = range(num_qbits)

    for layer in range(circ_depth - 1):  # exclude the last layer !

        if (layer + 1) % 2 == 1:  # odd layer
            for qbit in lst_qbits:
                var_circ.rx(theta[layer][qbit], qbit)

            for qbit in lst_qbits:
                if qbit == num_qbits - 1:  # the last one
                    pass

                elif qbit % 2 == 0:
                    var_circ.cx(qbit, qbit + 1)

        else:  # even layer
            for qbit in lst_qbits:
                var_circ.ry(theta[layer][qbit], qbit)

            for qbit in lst_qbits:
                if qbit == num_qbits - 1:  # the last one
                    pass

                elif qbit % 2 == 1:
                    var_circ.cx(qbit, qbit + 1)

    for qbit in lst_qbits:  # bonus layer at the end only has rx gates
        var_circ.rx(theta[circ_depth - 1][qbit], qbit)

    if debug:
        print(var_circ)

    return var_circ


def simulate_circ(circ):
    backend = Aer.get_backend('statevector_simulator')   # get simulator
    job = execute(circ, backend)
    result = job.result()
    print(type(result))
    # circ1_statevect = result1.get_statevector(circ1)


def main():
    # theta = qml_main.initialize_theta(num_qbits=5)
    # construct_variational_circ(theta, num_qbits=5)
    return


if __name__ == '__main__':
    main()
