#!/bin/bash

IMAGE=decotengu

docker container run \
  --name decotengu \
  --rm -it \
  -v decodata:/data \
  $IMAGE ash

