docker run \
    -it \
    --rm \
    -v $(pwd):/home/project \
    -w /home/project \
    --privileged \
    mgudim/mc
