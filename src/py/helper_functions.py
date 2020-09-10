# -*- coding: utf-8 -*-
from pathlib import Path

import numpy as np
import scipy.sparse as sparse
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, normalize


def make_log_maxn_tensor(mtx: sparse.csr.csr_matrix) -> tf.SparseTensor:
    """Convert a sparse matrix to a log x+1 normalised sparse tensor

    Parameters
    ----------
    mtx : sparse.csr.csr_matrix
        The sparse, raw count matrix

    Returns
    -------
    tf.SparseTensor
        A log x+1 normalised Sparse Tensor
    """

    # Normalise data
    mtx.data = np.log1p(mtx.data)
    mtx = normalize(mtx, norm="max", axis=1, copy=False)

    # Convert to Sparse tensor
    mtx = mtx.tocoo()
    indices = np.mat([mtx.row, mtx.col]).transpose()
    mtx = tf.SparseTensor(indices, mtx.data, mtx.shape)
    mtx = tf.sparse.reorder(mtx)

    return mtx


def init_label_encoder(labels: Path) -> LabelEncoder:
    """Constructed a label encoder from saved labels

    Parameters
    ----------
    labels: Path
        pathlib.Path to the saved labels. A .npy file is expected.

    Returns
    -------
    LabelEncoder
        An initialised sklearn.preprocessing.LabelEncoder
    """

    label_encoder = LabelEncoder()
    label_encoder.classes_ = np.load(labels)

    return label_encoder
