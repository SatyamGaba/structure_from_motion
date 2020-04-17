# CSE152B HW1, Q1 - SfM with libviso2

## Installation instructions
### 1. Set up the environment
#### [Option 1] On your own machine
- Install SWIG
    - On Ubuntu: `sudo apt-get install swig`, on MacOS: `brew install swig`
        - You need to install Homebrew first by [HomeBrew](https://brew.sh/)
- Install Python 3.X and Pip
- [Recommended] Create an environment (e.g. [Anaconda](https://docs.conda.io/en/latest/miniconda.html))
    - ``conda create --name pytorch36 python=3.6 pip``
    - ``conda activate pytorch36``
    
#### [Option 2] On the ``ieng6.ucsd.edu`` server
- Login with your credentials. You should enter a node with 1 GPU.
- Launch the environment
    - ``launch-scipy-ml-gpu.sh``
- Create an environment with conda
    - ``conda create --name pytorch36 python=3.6 pip``
    - ``conda activate pytorch36``
        - If you seeing errors activating the env, follow the information by typing `conda init bash`, `exit` and again ``launch-scipy-ml-gpu.sh``, then ``conda activate libvisio``
- Install SWIG
    - ``conda install swig``
    
### 2. Pull the libviso2 with Python wrappers repo and install dependencies
- ``git clone https://github.com/Jerrypiglet/pyviso2.git``
- Install dependencies (Python 3.X with Pip)
    - ``pip install -r requirements.txt``
- Compile and install pyviso
    - ``cd src/``
    - ``pip install -e .``

## Get the data
Change the dataset path in Line 26 to your paths. 

On the ``ieng6.ucsd.edu`` server, the dataset is located at `/datasets/cse152-252-sp20-public/dataset_SfM`.


## How to run
``python demo_viso_mono.py``

**Two toggles in Line 22-23 allows you to enable/disable the visualization, and to specify if the visualization will be display on screen or saved in the background.**

If ``if_vis == True`` and ``if_on_screen == True``, You should see something like this:
![](demo.png)

The errors are printed and the visualizations are saved at ``vis/``.


## [Extra] How to run training sessions
