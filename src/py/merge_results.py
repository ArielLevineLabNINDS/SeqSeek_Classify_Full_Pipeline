# -*- coding: utf-8 -*-
from pathlib import Path

import numpy as np
import pandas as pd

results = Path("results")
results.mkdir(parents=True, exist_ok=True)

coarse_types = pd.read_csv(
    results / "coarse_types.csv", names=["cell", "predicted.id"], header=0
)
neural_types = pd.read_csv(results / "neural_types.csv", names=["predicted.id"])

neural_types.loc[neural_types["predicted.id"] == "Garbage", "predicted.id"] = "Doublets"

coarse_types.loc[
    np.isin(coarse_types["predicted.id"], ["Motorneuron", "Neuron", "Doublets"]),
    "predicted.id",
] = neural_types.loc[:, "predicted.id"].to_numpy()

coarse_types.to_csv(results / "final_types.csv", index=False)
