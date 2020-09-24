# -*- coding: utf-8 -*-
from pathlib import Path

import helper_functions as hf
import numpy as np
import pandas as pd
import tensorflow as tf
from scipy.io import mmread

results = Path("results")
results.mkdir(parents=True, exist_ok=True)

models = Path("models")

# Read in the count matrix
# mmread only excepts strings or open files, so use open file
# Open file + Path = OS safe
print("Reading count matrix")
with open(results / "query_neural_counts.mtx", "rb") as file:
    counts = mmread(file)

# Filter genes where n_counts < 1
query_genes = pd.read_csv(results / "query_neural_features.csv").loc[:, "x"].to_numpy()
ref_genes = (
    pd.read_csv(models / "filter_NN_genes.tsv", sep="\t", names=["x"])
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
model = tf.keras.models.load_model(models / "neurons_doublets.model")
model.summary()

# Predict
print("Making predictions")
preds = np.argmax(model.predict(counts), axis=1)

# And convert to labels
le = hf.init_label_encoder(models / "dirty_neuron_encoder.npy")
preds = le.inverse_transform(preds)

# Finally, save results
np.savetxt(results / "neural_types.csv", preds, delimiter=",", fmt="%s")
