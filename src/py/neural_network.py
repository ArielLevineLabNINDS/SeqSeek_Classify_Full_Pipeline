# -*- coding: utf-8 -*-
import helper_functions as hf
import numpy as np
import pandas as pd
import tensorflow as tf
from scipy.io import mmread

# Read in the count matrix
print("Reading count matrix")
counts = mmread("results/query_neural_counts.mtx")

# Filter genes where n_counts < 1
query_genes = (
    pd.read_csv("results/query_neural_features.csv").loc[:, "x"].loc[:, "x"].to_numpy()
)
ref_genes = (
    pd.read_csv("models/filter_NN_genes.tsv", sep="\t", names=["x"])
    .loc[:, "x"]
    .to_numpy()
)

mask = np.isin(query_genes, ref_genes)

counts = counts.tocsc()[:, mask]
counts = counts.tocsr()

# Convert to tensor
counts = hf.make_log_maxn_tensor(counts)

# Load model
print("Loading model")
model = tf.keras.models.load_model("models/neurons_doublets.model")
model.summary()

# Predict
print("Making predictions")
preds = np.argmax(model.predict(counts), axis=1)

# And convert to labels
le = hf.init_label_encoder("models/dirty_neuron_encoder.npy")
preds = le.inverse_transform(preds)

# Finally, save results
np.savetext("results/neural_types.csv", preds, delimiter=",")
