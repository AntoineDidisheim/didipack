from didipack.utils_didi.smart_algebra import smart_eigenvalue_decomposition_covariance
import numpy as np

def run_efficient_ridge(
        signals: np.ndarray,
        labels: np.ndarray,
        shrinkage_list: list,
        ):
    eigval, eigvec = smart_eigenvalue_decomposition_covariance(features=signals)
    mu = (signals * labels.reshape(-1, 1)).mean(0).reshape(-1, 1)
    multiplied = np.matmul(eigvec.T, mu)  # for a window of 2000 and 4000 signals, the cost is 4000 * 4000
    normalized = np.concatenate([(1 / (eigval + z)).reshape(-1, 1) * multiplied for z in shrinkage_list], axis=1)
    # here it is subtle as the dimension of eigvec might be lower than that of beta !!!
    # but normalized has the right dimension !!
    betas = np.matmul(eigvec, normalized).T
    return betas


def smart_eff_weights_no_q(f_ins, z_grid, n_):
    """
    Compute efficient weights from in-sample factor returns using smart_inverse_times_vector

    :param f_ins: the signals coming in this function are equivalent to (R*S).groupby(date).sum(), except for line 21 and alike where it's (R*S).groupby(date).mean()
    (as discussed I multiplied the old factors by n_(
    :param z_grid: gris of shrinkage parameters
    :param n_: a vector of dim T by 1. Containing for each date in the rolling window the number of observations n.
    if n_ is None, I am pricing the fama factors.
    :return:
    :rtype:
    """

    if n_ is not None: # in the current setup, if n_ is None it means we are with the fama french.
        f_ins = f_ins * np.sqrt(n_)

    t_, p1 = f_ins.shape
    if p1 > t_:
        b_t_tilde = f_ins @ f_ins.T / t_
        eigenvalues_b_t_tilde, eigenvectors_b_t_tilde = np.linalg.eigh(b_t_tilde)
        if (eigenvalues_b_t_tilde < 0).any():
            print("Negative eigenvalues encountered! Check f_ins where there are factor returns are identical")
            print("For now, use the slow traditional method")
            eigenvalues_b_t_, eigenvectors_b_t = np.linalg.eigh((f_ins.T @ f_ins) / t_) # removed /n_.
            eigenvectors_b_t = eigenvectors_b_t[:, -t_:]
        else:
            eigenvectors_b_t = (f_ins.T @ eigenvectors_b_t_tilde) * (eigenvalues_b_t_tilde ** (-0.5)).reshape(1,-1) / np.sqrt(t_) # TODO ask semyon to checkif I was right to remove n as well
    else:
        eigenvalues_b_t_tilde, eigenvectors_b_t_tilde = np.linalg.eigh((f_ins.T @ f_ins) / t_) # Todo I'm assuming it's ok but here too, I removed the n_
        eigenvectors_b_t = eigenvectors_b_t_tilde

    if n_ is None:
        f_mean = f_ins.mean(axis=0).reshape(-1, 1)
    else:
        f_mean = (f_ins*np.sqrt(n_)).mean(axis=0).reshape(-1, 1)
    eff_weights = np.array([smart_inverse_times_vector(z_, eigenvectors_b_t, eigenvalues_b_t_tilde, f_mean) for z_ in z_grid]).T # Todo here too I removed the divided by n_

    return eff_weights.squeeze() # , eigenvalues_b_t_tilde, eigenvectors_b_t_tilde


def smart_inverse_times_vector(z_: float,
                               eigenvectors_b_t: np.ndarray,
                               eigenvalues_without_zeros: np.ndarray,
                               vector: np.ndarray):
    """
    This is a function that uses spectral decomposition to do (zI+B)^{-1}v = U (z+D)^{-1}U' v+(I-UU') z^{-1} v
    Parameters
    ----------
    z_
    eigenvectors_b_t
    eigenvalues_without_zeros
    vector

    Returns
    -------

    """
    mult1 = eigenvectors_b_t.T @ vector

    multiplied = (1 / (z_ + eigenvalues_without_zeros)).reshape(-1, 1) * mult1
    term1 = eigenvectors_b_t @ multiplied
    # this is a correction accounting for missing zero eigenvalues
    term2 = (1 / z_) * (vector - eigenvectors_b_t @ mult1)
    return term1 + term2