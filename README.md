# CSE152B HW1, Q1 - SfM with libviso2

## 1. Installation instructions
### 1. Set up the environment
#### 1. [Option 1] On your own machine
- Install SWIG
    - On Ubuntu: `sudo apt-get install swig`, on MacOS: `brew install swig`
        - You need to install Homebrew first by [HomeBrew](https://brew.sh/)
- Install Python 3.X and Pip
- [Recommended] Create an environment (e.g. [Anaconda](https://docs.conda.io/en/latest/miniconda.html))
    - ``conda create --name py36 python=3.6 pip``
    - ``conda activate py36``
    
#### 2. [Option 2] On the ``ieng6.ucsd.edu`` server
- Login with your credentials
    - `ssh {USERNAME}@ieng6.ucsd.edu`
- Launch your pod. You should enter a node with 1 GPU
    - ``launch-scipy-ml-gpu.sh``
- Create an environment with conda
    - ``conda create --name py36 python=3.6 pip``
    - ``conda activate py36``
        - If you seeing errors activating the env, follow the information on screen by typing `conda init bash`, `exit` and again ``launch-scipy-ml-gpu.sh``, then ``conda activate py36``
- Install SWIG
    - ``conda install swig``
    
### 2. Pull the repo and install dependencies
- ``git clone https://github.com/Jerrypiglet/pyviso2-SfM.git``
- Install dependencies (Python 3.X with Pip)
    - ``pip install -r requirements.txt``
- Compile and install pyviso
    - ``cd src/``
    - ``pip install -e .``

## 2. Get the data
Change the dataset path in Line 26 to your paths. 

On the ``ieng6.ucsd.edu`` server, the dataset is located at `/datasets/cse152-252-sp20-public/dataset_SfM`.

## 3. How to run
``python demo_viso_mono.py``

**Two toggles in Line 22-23 allows you to enable/disable the visualization, and to specify if the visualization will be display on screen or saved in the background.**

If ``if_vis == True`` and ``if_on_screen == True``, You should see something like this:
![](demo.png)

The errors are printed and the visualizations are saved at ``vis/``. To fetch the files you can use commands like `scp` to transfer files to your local machine, or from the cluster to your local machine:

``scp -r <USERNAME>@dsmlp-login.ucsd.edu:/datasets/cse152-252-sp20-public/dataset_SfM .``



## 4. [Extra] How to run training sessions

### 1. Set up the environment

#### [Option 1] On the ``ieng6.ucsd.edu`` server

- Login with your credentials
    - `ssh {USERNAME}@ieng6.ucsd.edu`

-  Launch TMUX
    - Reconmended for session management: you can come back anytime after you disconnect your session. Otherwise you have to keep your connection on for hours while training.
    - Just run ``tmux``
    - To detach and come back later, use `ctrl + b` then `d`. To attach next time, use `ctrl + b` then `a`.
    - For more TMUX usages please refer to online tutorials like [https://linuxize.com/post/getting-started-with-tmux/](https://linuxize.com/post/getting-started-with-tmux/)

-  Launch your pod
    - `launch-scipy-ml-gpu.sh`

#### [Option 2] On your own server
Just launch TMUX.

### 2. Start training
Now you can create conda env and do your training in there following Section 1.1

