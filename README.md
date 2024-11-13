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

1. Ensure that you have Conda installed on your system.
Please refer to the [official documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) for installation and usage.
If you need additional help, we recommend asking a large language model such as ChatGPT or Claude.

2. Navigate into the project directory and run the following command:

`conda env create -f environment.yml`

This will create a conda environment called `op_note`.

3. Activate the environment by entering `conda activate op_note`.

## Usage
To run the classification model, use the following command:

Toy dataset provided: `op_note_sample.csv`

<details>
    <summary>Using Llama for inference
    
    We used Llama3.1 models through Ollama.
    For this, you will need to open two terminals on the same computer as one process will run the server.
    This can be done with two separate windows (or terminal tabs or a terminal multiplexer like Tmux).

    1. Install Ollama on your computer system.
    - Test this using `ollama serve`. This will start a server if it is installed properly.

    2. On one terminal, start the server with `ollama serve`.

    3. On the second terminal, pull the models you want with a command like `ollama pull llama3.1:70b`.

    4. On the same terminal, activate the conda env (`conda activate op_note`) and run `python 04_llama_model.py`.
</details>

## Contributing
Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more information.

## Contact
For questions or feedback, please contact [Jeremy Balch](mailto:jeremy.balch@surgery.ufl.edu).
