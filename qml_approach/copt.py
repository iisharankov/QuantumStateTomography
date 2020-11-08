# classical optimization suite
import numpy as np
import scipy.optimize as opt
import qpu
optimizer_data = []
optimizer_len = 0  # global constants to store info from optimizer calls


def get_fidelity(theta, psi):
    """
    compute the fidelity between two quantum states (psi, phi) where
    psi is the target state and phi is the reconstructed state generated
    using VQCs.

    :param theta: np.array, containing the parameterization for the VQC
    :param psi: qiskit.QuantumCircuit object, target state psi
    :return: float, fidelity between (0, 1)
    """

    circ = qpu.construct_variational_circ(theta)
    phi = qpu.simulate_circ(circ)
    fidelity = qpu.compute_fidelity(psi, phi)

    return fidelity


def get_loss(fidelity):
    """
    Get the loss between two states given the fidelity between them.
    We define the loss between two states as 1 - sqrt(fidelity).

    :param fidelity: float
    :return: float, loss
    """

    return 1 - np.sqrt(fidelity)


def compute_loss(theta_vector, *args):
    """
    Compute the loss explicitly between two states (psi, phi). Where phi
    is reconstructed from the parameterization theta. args is a list containing
    the target state psi, the variational circuit depth and the number of qbits in
    psi.

    :param theta_vector: np.array, the parameterization vector
    :param args: list, containing [psi, circ_depth, num_qbits]
    :return: float, loss
    """

    psi = args[0]
    circ_depth = args[1]
    num_qbits = args[2]
    theta = np.reshape(theta_vector, (circ_depth, num_qbits))

    fidelity = get_fidelity(theta, psi)
    loss = get_loss(fidelity)
    return loss


def compute_loss_gradient(theta_vector, *args):
    """
    Compute the gradient of our loss function. Since the loss is a scalar function
    over a vector parameter (thetas) we will have a vector valued gardient. We compute
    the gradient evaluated at (theta_vector). args is a list which contains the target state
    psi (qiskit.QuantumCircuit object), the variational quantum circuit depth, and the number
    of qbits.

    :param theta_vector: np.array, the parameterization vector
    :param args: list, contains [psi, circ_depth, num_qbits]
    :return: np.array, of len = len(theta_vector), the gradient vector
    """

    psi = args[0]  # feed psi as a parameter
    circ_depth = args[1]
    num_qbits = args[2]
    theta = np.reshape(theta_vector, (circ_depth, num_qbits))  # reshapes the flat theta vector
    fidelity = get_fidelity(theta, psi)

    # the derivative of the loss wrt fidelity
    dl_df = -0.5 * fidelity ** (-0.5)

    df_dtheta = []  # a list of partial derivatives of the fidelity wrt the theta parameters

    for index in range(len(theta_vector)):
        layer_index = index // num_qbits
        qbit_index = index % num_qbits

        theta_plus = np.copy(theta)
        theta_plus[layer_index][qbit_index] += np.pi / 2  # added pi/2 to the ith theta parameter

        theta_minus = np.copy(theta)
        theta_minus[layer_index][qbit_index] -= np.pi / 2  # subtracted pi/2 to the ith theta parameter

        df_dtheta_i = 0.5 * (get_fidelity(theta_plus, psi) - get_fidelity(theta_minus, psi))  # ith derivative
        df_dtheta.append(df_dtheta_i)

    df_dtheta = np.array(df_dtheta)
    dl_dtheta = dl_df * df_dtheta  # chain rule to get partial derivative of loss wrt theta parameters

    return dl_dtheta


def optimizer_callback(current_theta):
    """
    A function to store the state of the parameterization (theta) vector as it
    gets optimized. This data is useful for tuning the optimization process.

    :param current_theta: np.array, current iteration value of theta_vector
    :return: bool, False constantly to prevent optimizer from truncating early
    """

    global optimizer_data
    global optimizer_len

    optimizer_data.append(current_theta)
    optimizer_len += 1
    return False


def optimize_theta_scp(theta, psi):
    """
    A function that determines the optimal parameterization vector (theta) for a
    variational quantum circuit in order to minimize the loss (the difference)
    between a target state psi and a reconstructed state phi (produced from theta)

    :param theta: np.array, parameterization vector
    :param psi: qiskit.QuantumCircuit object, target state psi
    :return: results from optimizer and list (optimizer data), which contains results between each iteration
    """

    theta_vector = np.reshape(theta, theta.size)
    circ_depth, num_qbits = theta.shape
    global optimizer_data

    results = opt.minimize(compute_loss, theta_vector, args=(psi, circ_depth, num_qbits), method='BFGS',
                           jac=compute_loss_gradient, callback=optimizer_callback, options={'maxiter': 100})

    return results, optimizer_data


def reset():
    """
    function to manually reset the globabl variables.
    Should not be used (only for emergancies)
    :return: None
    """

    global optimizer_data
    global optimizer_len

    optimizer_data = []
    optimizer_len = 0
    return


def main():
    return


if __name__ == "__main__":
    main()
