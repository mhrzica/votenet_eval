# Container image that runs your code
FROM continuumio/miniconda3

RUN apt-get update -y && apt-get install libxml2 -y
# Create the environment:
COPY environment.yaml .
RUN conda env create -f environment.yaml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "votenet_clean", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
RUN echo "Make sure Python is installed:"
RUN python --version

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh

# Install cuda dependencies
# RUN conda install -c conda-forge cudatoolkit-dev
# RUN conda install pytorch==1.1.0 torchvision==0.3.0 cudatoolkit=10.0 -c pytorch
# RUN conda install cudnn=7.6.0
RUN pip3 install tensorflow-gpu==1.14

# Check if everything is installed
# RUN conda list cudnn
# RUN conda list cudatoolkit

# Check if GPU is available
RUN echo "Check if GPU is available"
RUN python -c 'import tensorflow as tf; print(tf.__version__); tf.test.is_gpu_available()'

# Code file to execute when the docker container starts up (`entrypoint.sh`)
# ENTRYPOINT ["/entrypoint.sh"]
ENTRYPOINT ["conda", "run", "-n", "votenet_clean", "python", "--version"]
