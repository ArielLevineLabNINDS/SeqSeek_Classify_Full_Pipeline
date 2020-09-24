# The Seq-Seek Pipeline

This repository provides the code for users to run the pipeline outline in [Daniel E. Russ<sup>1,\*</sup>, Ryan B. Patterson-Cross<sup>2,\*</sup>, et al., _biorXiv_, 2020](https://www.biorxiv.org/content/10.1101/2020.09.03.241760v1.full).

## Usage

Broadly speaking, this pipeline has 2 steps:

1. Use Label Transfer within Seurat to predict the coarse cell types present.
2. Use a Neural Network built with Keras to predict the neural subtypes present.

To make the pipeline as smooth as possible, this project uses Data Version Control, also known as [DVC](https://www.dvc.org) to run the steps automatically and handle the data processing. For more information on the instricacies of DVC, please see the above link to the project's website. To run the pipeline, please follow the steps below.

### 1. Get the code

First, fetch the repository from github. To do so, run the following command:

```bash
git clone https://www.github.com/ArielLevineLabNINDS/SeqSeek_Pipeline
```

Once it's fetched, move into the directory:

```bash
cd SeqSeek_Pipeline && ls
```

### 2. Get the Data

As the reference data object is fairly large, it cannot be stored directly on github. It's located on our [SeqSeek website](http://www.seqseek.ninds.nih.gov/). Don't let that bother you, though. The beauty of DVC is that it can run all kinds of steps as part of the pipeline, so the reference data will be automatically downloaded for you. Do note that, even after stripping out all un-essential information, it is still a large file at ~ 1.5 Gb.

The query object can be any dataset of spinal cord cells that you provide. Move it into the data folder as well, and make sure it is called, apropriately enough, `data/query.rds`. Per the recommendations in the [Seurat vignette](https://satijalab.org/seurat/v3.0/integration.html), make sure your data has been normalised and variable features found, but not scaled!

Currently, this pipeline requires that your query is aligned to the same genome as ours. The metadata from the genome is provide below:

> mm10_10X_premrna_1 dna:chromosome chromosome:GRCm38:1:1:195471971:1 REF
> !genome-build GRCm38.p4
> !genome-version GRCm38
> !genome-date 2012-01
> !genome-build-accession NCBI:GCA_000001635.6
> !genebuild-last-updated 2016-01

Work is on-going to build in an adaptor that handles all genomes. Until then, please align using the same genome!

### 3. Create a Python Virtual Environment

It's best practice to install dependencies for Python Projects within a virtual environment. There are many different methods for creating and managing virtual environments. If you already have a method that you use in your workflow, then please create and activate the virtual environment that way.

If you don't have a preference, the following will create and activate a virtual environment on MacOS or Linux:

```bash
python3 -m venv SeqSeek
source SeqSeek/bin/activate
```

On a Windows system, it's a little different. In Windows, run the following:

```bash
python3 -m venv SeqSeek
SeqSeek\Scripts\activate.bat
```

Once the environment has been created and activated, install the necessary dependencies via `pip`, as below:

```bash
pip install -r requirements.txt
```

At this point, verify that installation has worked correctly by running the following command:

```bash
dvc --version
```

The output should look like `1.6.6` - the exact number may vary, depending on the most up-to-date version. If you see anything else, or an error message, please let us know by filling an issue [HERE](https://github.com/ArielLevineLabNINDS/SeqSeek_Pipeline/issues), and we will get back to you as soon as we can!

### 4. Run the Pipeline

Thanks to DVC, running the pipeline is quite straight forward. Just use the below command:

```bash
dvc repro
```

And everything should take care of itself. You'll see message printed along the way to let you know what steps you are on. The predicted labels will be stored as `results/final_cell_types.csv`. There will be 2 columns: `cell` and `class`. The first contains the name of the cell taken from the Seurat object, and the second the predicted cell type. Also, this information will be added as a metadata column named "predicted.id" to the original Seurat object. This updated Seurat object will be saved at `results/query.rds` to prevent conflicts.

If you run into any issues, please let us know [HERE](https://github.com/ArielLevineLabNINDS/SeqSeek_Pipeline/issues).
