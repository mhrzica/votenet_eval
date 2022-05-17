ARG FROM_IMAGE_NAME=nvidia/cuda:11.1-devel-ubuntu18.04
FROM ${FROM_IMAGE_NAME}

# Installation of some libraries / RUN some commands on the base image
ENV DEBIAN_FRONTEND noninteractive
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates \
    build-essential python3-pip python3-dev wget git sudo &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

#OpenGLW
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENV TORCH_CUDA_ARCH_LIST='8.0+PTX'

#OpenGL
RUN apt-get update \
    && apt-get install -y -qq --no-install-recommends \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libxext6 \
    libx11-6 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

#Installation of build essential
RUN apt-get install build-essential

#Cmake
RUN apt-get update -q
RUN apt-get upgrade -y
RUN apt-get install -y libprotobuf-dev protobuf-compiler
RUN apt-get install -y cmake

RUN apt-get update && apt-get install -y nano

ENV PATH="/root/.local/bin:${PATH}"
RUN wget https://bootstrap.pypa.io/pip/3.6/get-pip.py && \
    python3 get-pip.py --user && \
    rm get-pip.py

RUN pip install --user tensorboard
RUN pip install --user torch==1.8.0+cu111 torchvision==0.9.0+cu111 torchaudio==0.8.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install tensorflow-gpu==1.14

RUN pip install matplotlib
RUN pip install plyfile
RUN pip install opencv-python
RUN pip install trimesh
RUN pip install scipy

# set FORCE_CUDA because during `docker build` cuda is not accessible
ENV FORCE_CUDA="1"
# This will by default build detectron2 for all common cuda architectures and take a lot more time,
# because inside `docker build`, there is no way to tell which architecture will be used.
ARG TORCH_CUDA_ARCH_LIST="Kepler;Kepler+Tesla;Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"
ENV TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST}"

COPY ./ $HOME/votenet/

RUN cd /votenet/pointnet2 && python3 setup.py install

ENTRYPOINT [ "/bin/bash", "run_eval.sh" ]
