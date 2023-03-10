# Tetris AI using a Deep Reinforcement Learning
This projects implementes a Tetris AI using a double deep Q-learning.

## Requirements
- Current version of Python3 (I used Python 3.10)
- Jupyter Notebook/Lab
- The package manager [pip](https://pip.pypa.io/en/stable/)

Use pip to install the dependencies:

```bash
pip install numpy pandas tqdm ipywidgets wandb pygame torch
```

Tested with Ubuntu 22.04.

## Installation

Clone the project using git.

Extract the file `replays.zip` in the directory `pro-replays` so the all the `.json` files lie directly in the `pro-replays` directory. This is needed since unzipped those files are nearly 250MB in size, while zipped only about 9MB.

## Usage

Open the cloned folder in Jupyter. The main learning approach is in the file `dqn.ipynb`.

After training an agent with the `dqn.ipynb` notebook and saving it to the `models` directory, this agent can be used to render a run using the `run-renderer.ipynb`. You just have to change the name of the saved/loaded model accordingly in both notebooks.

A pretrained agent's weights can be found in `models/good-cnn-1.pt` and `models/good-cnn-2.pt`. By providing those files to the `run-renderer.ipynb` one can watch them play.

## Folder Structure
- **dqn.ipynb**: the main file that implements the double deep Q-learning approach
- **run-renderer.ipynb**: uses learned model weights to simulate a game played by the agent and renders it in a graphical interface (using pygame)
- **tetris/**: contains the implementation of the game
- **gui/**: contains the code for the GUI renderer
- **util/**: helpers (currently only implementation for decay-functions)
- **models/**: contains the learned weights for selected runs



# Demo
To get to the better quality and longer youtube video version, click on the GIFs. 

## CNN
[![Tetris AI - Convolutional Neuronal Network](videos/CNN.gif)](http://www.youtube.com/watch?v=tB4wjei0FRo "Tetris AI - Convolutional Neuronal Network")

> Note: The genetic approach version can currently be found in the `genetic` branch of this repository.

## Genetic Singles
[![Tetris AI - Genetic Algorithm v1](videos/genetic-singles.gif)](http://www.youtube.com/watch?v=dT_M6IO00Pk "Tetris AI - Genetic Algorithm v1")


## Genetic Quads
[![Tetris AI - Genetic Algorithm v2](videos/genetic-quads.gif)](http://www.youtube.com/watch?v=jwAjfjrOvPo "Tetris AI - Genetic Algorithm v2")
