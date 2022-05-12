#!/bin/bash
echo "Hello!"
# code skripta.sh

conda create --name votenet_clean python=3.6 anaconda
source activate votenet_clean

conda install -c conda-forge cudatoolkit-dev
conda install pytorch==1.1.0 torchvision==0.3.0 cudatoolkit=10.0 -c pytorch
conda install cudnn=7.6.0

# check supported versions of cudnn for cuda builds
# conda search cudnn

pip3 install tensorflow-gpu==1.14

#Check if installed
conda list cudnn
conda list cudatoolkit

#jos sam testirala u pythonu
python -c 'import tensorflow as tf; print(tf.__version__); tf.test.is_gpu_available()'

pip install -r requirements.txt

cd pointnet2
python setup.py install




# Compatibile tensorflow versions: https://cdn-images-1.medium.com/max/1000/1*pyZAEgX30F09Fgt9jksB-Q.png
# Pytorch versions: https://pytorch.org/get-started/previous-versions/#v110
