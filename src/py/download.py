# -*- coding: utf-8 -*-
from pathlib import Path

import requests

# Make sure target directory exists
data = Path("data")
data.mkdir(parents=True, exist_ok=True)

# Make request
print("Requesting reference from website. This may take awhile...")
url = "https://seqseek.ninds.nih.gov/data/classify/reference.rds"
r = requests.get(url)

# Download
print("Downloading reference. This may take awhile...")
with open(data / "reference.rds", "wb") as file:
    file.write(r.content)
