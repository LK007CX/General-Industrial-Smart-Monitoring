#!/bin/bash
xhost +
docker run -it \
--net=host \
--privileged \
--runtime nvidia \
-e DISPLAY=$DISPLAY \
-v appconfig:/app/appconfig \
--mount type=bind,source=/home/auo/app/gism/model,target=/app/custom_model \
gism:v1.5
