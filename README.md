# ufl_op_note_multi_label_classification
Companion code to "Large Language Models for Multi-label Document Classification for Surgical Concepts in Exploratory Laparotomy Operative Notes"

# ufl_op_note_multi_label_classification

Companion code to "Large Language Models for Multi-label Document Classification for Surgical Concepts in Exploratory Laparotomy Operative Notes"

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction
This project provides a framework for multi-label document classification using large language models. We use the data from the [Exploratory Laparotomy Project](https://github.com/ufl-prismap/exploratory-laparotomy-project) to train and evaluate models for classifying surgical concepts in exploratory laparotomy operative notes.

## Features
- Multi-label classification   
- Iterative stratification of data for training and evaluation
- Baseline comparison to BoW and tf-idf models
- Fine-tuning and inference code for Longformer and Llama 3.2 models
- Evaluation script for visualization of model performance 


## Installation
To install the necessary dependencies

1. Ensure that you have Conda installed on your system

2. Navigate into the project directory and run the following command:

`conda env create -f environment.yml`

This will create a conda environment called `op_note`.

3. Activate the environment by entering `conda activate op_note`.

## Usage
To run the classification model, use the following command:

Toy dataset provided: `op_note_sample.csv`

## Contributing
Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more information.

## Contact
For questions or feedback, please contact [Jeremy Balch](mailto:jeremy.balch@surgery.ufl.edu).
