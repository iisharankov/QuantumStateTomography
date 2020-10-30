"""Quantum Machine Learning

Allows user to run QML with varying parameters.
"""

import numpy as np
import os
import sys

backend = os.path.dirname(os.path.abspath(__file__))
qml_approach = os.path.join(os.path.dirname(backend), 'qml_approach')
sys.path.insert(1, qml_approach)

import qpu
import qml_main
import copt


def _get_phis(circ_depth, num_qbits):
    print('get_phis', 'circ_depth =', circ_depth, ' num_qbits =', num_qbits)

    # randomly select a target state |psi>
    psi = qml_main.generate_random_psi(num_qbits=num_qbits)
    # initialize the parameters of our variational circuit
    initial_theta = qml_main.initialize_theta(
        circ_depth=circ_depth, num_qbits=num_qbits)
    # Final result
    results, optimizer_data = copt.optimize_theta_scp(initial_theta, psi)

    # Get loss and fidelity
    loss_series = []
    fidelity_series = []
    phis = []

    for optimizer in optimizer_data:
        theta = np.reshape(optimizer, (circ_depth, num_qbits))
        fidelity = copt.get_fidelity(theta, psi)
        loss = copt.get_loss(fidelity)

        loss_series.append(loss)
        fidelity_series.append(fidelity)
        phis.append(qpu.get_state(theta))

    return loss_series, fidelity_series, phis


def _export_phi(phi):
    result = phi.to_dict()
    for key, value in result.items():
        # Drop surrounding brackets ( )
        result[key] = [value.real, value.imag]

    return result


def _get_max_mag(phi):
    result = phi.to_dict()
    return max(abs(num) for num in result.values())


def show_phis(kwargs):
    loss_series, fidelity_series, phis = _get_phis(**kwargs)

    serialized_phis = []
    for phi in phis:
        serialized_phis.append(_export_phi(phi))

    output = {
        'fidelity_series': fidelity_series,
        'loss_series': loss_series,
        'maxMag': _get_max_mag(phis[-1]),
        'phis': serialized_phis,
    }

    return output
