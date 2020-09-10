# -*- coding: utf-8 -*-
import numpy as np
import scipy.sparse as sparse
import tensorflow as tf
from scipy.io import mmread

import src.py.helper_functions as hf

# Read in the count matrix
print('Reading count matrix')
counts = mmread("results/query_neural_counts.mtx")
if sparse.isspmatrix_coo(counts):
    counts = counts.tocsr()

# Convert to tensor
counts = hf.make_log_maxn_tensor(counts)

# Load model
print('Loading model')
model = tf.keras.models.load_model("models/neurons_doublets.model")
model.summary()

# Predict
print('Making predictions')
preds = np.argmax(model.predict(counts), axis=1)

# And convert to labels
le = hf.init_label_encoder("models/dirty_neuron_encoder.npy")
preds = le.inverse_transform(preds)

# Finally, save results
np.savetext('results/neural_types.csv', preds, delimiter=',')
