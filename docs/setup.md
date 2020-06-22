# Setting up to run this code

After initial setup, the scripts in qol_scripts can be used to set up/teardown your environment, as long as this repo is stored in /src/fyp

### Cuda
1. Buy & install a decent nVidia GPU. If you need me to explain this to you, you're fucked. 
1. Install NVIDIA CUDA Toolkit, available at http://developer.nvidia.com/cuda-downloads. On Ubuntu 18.04 x86_64, the instructions are as follows:

```
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
sudo mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /"
sudo apt-get updatesudo apt-get -y install cuda
```

If you run into issues, try sudo apt install nvidia-cuda-toolkit.

### Devenv
1. Install Python3, Git, and Anaconda.
1. init conda environment:
  1. conda create -n fyp_devenv python=3.7 pandas scikit-learn  
  1. conda activate fyp_devenv
  1. conda install -c conda-forge jupyterlab 
  1. conda install -c conda-forge dvc ~~can these two be combined?~~
1. create data directory and add to gitignore. 
1. Initialise python notebook using `jupyter lab`, and access through browser.
1. Write code
1. ???
1. Profit
