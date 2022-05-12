#!/bin/sh -l

echo "Hello $1"
time=$(date)
echo "::set-output name=time::$time"

# Check Python versions
echo "Using Python version:"
python --version
pip install --upgrade pip

# Install conda
apt-get update
# apt-get install wget
# cd /tmp
# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
# bash ~/miniconda.sh -b -p $HOME/miniconda
# export PATH="/github/home/miniconda/bin:$PATH"

# Create conda environment
# conda create --name votenet_clean python=3.6 anaconda
# conda activate votenet_clean

conda install -c conda-forge cudatoolkit-dev
conda install pytorch==1.1.0 torchvision==0.3.0 cudatoolkit=10.0 -c pytorch
conda install cudnn=7.6.0

# check supported versions of cudnn for cuda builds
# conda search cudnn

pip3 install tensorflow-gpu==1.14

# Check if installed
conda list cudnn
conda list cudatoolkit


# pip install -r requirements.txt
echo "#######################################################"
echo "Check if GPU is available"
echo "#######################################################"
python -c 'import tensorflow as tf; print(tf.__version__); tf.test.is_gpu_available()'
