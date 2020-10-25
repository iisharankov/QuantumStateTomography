# classical optimization suite
import numpy as np
import qml_main
import qpu
import tensorflow_probability as tfp


def get_fidelity(theta, psi):
    circ = qpu.construct_variational_circ(theta)
    phi = qpu.simulate_circ(circ)
    fidelity = qpu.compute_fidelity(psi, phi)

    return fidelity


def get_loss(fidelity):
    return 1 - np.sqrt(fidelity)


def wrap_psi(psi):
    def compute_loss_gradient(theta_vector):
        theta = np.reshape(theta_vector, (qpu.circ_depth, qpu.num_qbits))  # reshapes the flat theta vector
        fidelity = get_fidelity(theta, psi)
        loss = get_loss(fidelity)

        dl_df = -0.5 * fidelity ** (-0.5)  # the derivative of the loss wrt fidelity

        df_dtheta = []  # a list of partial derivatives of the fidelity wrt the theta parameters

        for index in range(len(theta_vector)):
            layer_index = index // qpu.num_qbits
            qbit_index = index % qpu.num_qbits

            theta_plus = np.copy(theta)
            theta_plus[layer_index][qbit_index] += np.pi / 2  # added pi/2 to the ith theta parameter

            theta_minus = np.copy(theta)
            theta_minus[layer_index][qbit_index] -= np.pi / 2  # subtracted pi/2 to the ith theta parameter

            df_dtheta_i = 0.5 * (get_fidelity(theta_plus, psi) - get_fidelity(theta_minus, psi))  # ith derivative
            df_dtheta.append(df_dtheta_i)

        df_dtheta = np.array(df_dtheta)
        dl_dtheta = dl_df * df_dtheta  # chain rule to get partial derivative of loss wrt theta parameters

        return loss, dl_dtheta
    return compute_loss_gradient


# def compute_loss_gradient(theta_vector, psi):
#     theta = np.reshape(theta_vector, (qpu.circ_depth, qpu.num_qbits))  # reshapes the flat theta vector
#     fidelity = get_fidelity(theta, psi)
#
#     dl_df = -0.5 * fidelity**(-0.5)      # the derivative of the loss wrt fidelity
#
#     df_dtheta = []   # a list of partial derivatives of the fidelity wrt the theta parameters
#     for index in range(len(theta_vector)):
#         theta_plus = np.copy(theta)
#         theta_plus[index] += np.pi / 2  # added pi/2 to the ith theta parameter
#
#         theta_minus = np.copy(theta)
#         theta_minus[index] -= np.pi / 2  # subtracted pi/2 to the ith theta parameter
#
#         df_dtheta_i = 0.5 * (get_fidelity(theta_plus, psi) - get_fidelity(theta_minus, fidelity))  # ith derivative
#         df_dtheta.append(df_dtheta_i)
#
#     df_dtheta = np.array(df_dtheta)
#     dl_dtheta = dl_df * df_dtheta  # chain rule to get partial derivative of loss wrt theta parameters
#
#     return dl_dtheta


def optimize_theta(theta, psi):
    theta_vector = np.reshape(theta, theta.size)
    value_grad_func = wrap_psi(psi)

    results = tfp.optimizer.bfgs_minimize(value_grad_func, theta_vector)
    final_theta_vector = results.position()
    final_theta = np.reshape(final_theta_vector, (qpu.circ_depth, qpu.num_qbits))

    return final_theta


def main():

    return


if __name__ == '__main__':
    main()
