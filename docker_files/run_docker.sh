docker rm votenet_v1
    #-e QT_X11_NO_MITSHM=1 \
docker run --gpus all --runtime=runc --interactive -it \
    --shm-size=8gb --env="DISPLAY" --volume="/home/dzijan/COSPER/Code/votenet/:/home/dzijan/COSPER/Code/votenet/" \
    --volume="/data/cospernet/:/home/dzijan/COSPER/Code/votenet/data/" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --workdir="/home/dzijan/COSPER/Code/votenet" \
	-p 6007:6007 \
    --name=votenet_v1 votenet:v1