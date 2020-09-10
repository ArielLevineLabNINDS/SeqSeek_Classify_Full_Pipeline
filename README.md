# The Seq-Seek Pipeline

This repository provides the code for users to run the pipeline outline in [Daniel E. Russ<sup>1,\*</sup>, Ryan B. Patterson-Cross<sup>2,\*</sup>, et al., _biorXiv_, 2020](FILLER PLEASE CHANGE).

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

As the reference data object is fairly large, it cannot be stored directly on github. Please download it [HERE](FILLER PLEASE CHANGE) and more it into the `data` folder in this project. It should be named `data/reference.rds` or the pipeline will be unable to find it!

The query object can be any dataset of spinal cord cells that you provide. Move it into the data folder as well, and make sure it is called, apropriately enough, `data/query.rds`.

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
SeqSeek\\Scripts\\activate.bat
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

And everything should take care of itself. You'll see message printed along the way to let you know what steps you are on. The predicted labels will be stored as `results/final_cell_types.csv`. There will be 2 columns: `cell` and `class`. The first contains the name of the cell taken from the Seurat object, and the second the predicted cell type.

If you run into any issues, please let us know [HERE](https://github.com/ArielLevineLabNINDS/SeqSeek_Pipeline/issues).
