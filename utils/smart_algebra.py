import numpy as np
def smart_eigenvalue_decomposition_covariance(features: np.ndarray):
    """
    Lemma 28: Efficient Eigen value decomposition
    :param n: normalization
    :param features: features used to create covariance matrix times x P
    :param T: Weight used to normalize matrix
    :return: Left eigenvectors PxT and eigenvalues without zeros
    """
    [T, P] = features.shape

    if P > T:
        covariance = features @ features.T /T

    else:
        covariance = features.T @ features / T

    eigval, eigvec = np.linalg.eigh(covariance)
    # eigvec = eigvec[:, eigval > 10 ** (-10)]
    # eigval = eigval[eigval > 10 ** (-10)]

    if P > T:
        # project features on normalized eigenvectors
        eigvec = features.T @ eigvec * (eigval ** (-1 / 2)).reshape(1, -1) / np.sqrt(T)

    return eigval, eigvec
