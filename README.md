# Tetris AI using a Genetic Algorithm

This projects implementes a Tetris AI using a genetic algorithm. 

## Requirements
- Current version of Python3 (I used Python 3.10)
- The package manager [pip](https://pip.pypa.io/en/stable/)

Use pip to install the dependencies:

```bash
pip install numpy matplotlib tqdm wandb pygame
```

## Installation

Clone the project using git.

## Usage

Open the cloned folder in Jupyter. The main learning approach is in the file `genetic.ipybn`.

## Folder Structure
- **genetic.ipynb**: the main file that implements the genetic algorithm
- **run-renderer.ipynb**: uses learned weights to simulate a game played by the agent and renders it in a graphical interface (using pygame)
- **tetris/**: contains the implementation of the game
- **gui/**: contains the code for the GUI renderer
- **util/**: helpers (currently only implementation for decay-functions)
- **models/**: contains the learned weights for selected runs
