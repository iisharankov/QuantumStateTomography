from qiskit import *


def construct_variational_circ(theta, debug=False):
    """
    Generate a parameterized variational quantum circuit
    :param theta: numpy array, tuning our parameters for the variational circuit
    :param debug: bool, prints info when debugging
    :return: qiskit.QuantumCircuit object, the variational circuit
    """
    circ_depth, num_qbits = theta.shape
    var_circ = qiskit.QuantumCircuit(num_qbits)
    lst_qbits = range(num_qbits)

    for layer in range(circ_depth - 1):
        for qbit in range(len(lst_qbits)):

            # Compute if layer is odd or even to apply rx or ry gate to circuit
            is_odd_step = (layer + 1) % 2
            if is_odd_step:
                var_circ.rx(theta[layer][qbit], qbit)
            else:
                var_circ.ry(theta[layer][qbit], qbit)

            # Apply a cx gate AFTER first 3 qbits processed
            if qbit % 2 == 0 and qbit != 0:

                # isOddStep may subtract 1 if True, to correctly apply cx gate location
                var_circ.cx(qbit - is_odd_step - 1, qbit - is_odd_step)

    for qbit in lst_qbits:  # bonus layer at the end only has rx gates and no cx
        var_circ.rx(theta[circ_depth - 1][qbit], qbit)

    if debug:
        print(var_circ)

    return var_circ


def simulate_circ(circ):
    """
    Generates our estimate state |phi> via simulation
    :param circ: qiskit.QuantumCircuit object, the variational quantum circuit
    :return: qiskit.Statevector object, represents our estimated quantum state |phi>
    """
    backend = Aer.get_backend('statevector_simulator')   # get simulator
    job = execute(circ, backend)
    result = job.result()
    circ_statevect = qiskit.quantum_info.Statevector(
        result.get_statevector(circ))

    return circ_statevect


def compute_fidelity(psi, phi):
    """
    Compute the fidelity (a measure of similarity) between the two states
    :param psi: qiskit.Statevector, our target state |psi>
    :param phi: qiskit.Statevector, our estimated state |phi>
    :return: float, fidelity
    """

    fidelity = qiskit.quantum_info.state_fidelity(psi, phi)
    return fidelity


def get_state(theta):
    """
    Use the parameter matrix (theta) to recreate state
    :param theta: np.array, describes the parameters in the variational circuit
    :return: qiskit.quantum_info.Statevector
    """
    circ = construct_variational_circ(theta)
    state = simulate_circ(circ)
    return state


def main():
    return


if __name__ == '__main__':
    main()
