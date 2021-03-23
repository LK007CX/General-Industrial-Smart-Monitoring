#!/bin/bash
xhost +
docker run -it \
--rm \
--net=host \
--runtime nvidia \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix/:/tmp/.X11-unix \
-v appconfig:/app/appconfig \
-v image:/app/image \
--mount type=bind,source=/home/edit/app/gism/model,target=/app/custom_model \
--privileged \
gism:v1.5.1
