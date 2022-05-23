FROM mgudim/llvmtoolchain

RUN apt-get install ninja-build
RUN apt-get install make
RUN apt-get install gcc -y
RUN apt-get install -y pkg-config
RUN apt-get update
RUN apt-get install -y libglib2.0-dev
RUN apt install git-all -y
RUN apt install libpixman-1-dev libcairo2-dev libpango1.0-dev libjpeg8-dev libgif-dev -y

ADD qemu /home/qemu
RUN cd /home/qemu/build && ../configure --target-list=riscv32-softmmu && make -j3 && make install

RUN apt install device-tree-compiler -y
RUN apt-get install gdb-multiarch -y

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get -y install python3-pip
RUN pip install -U pytest

# docker build . -t mgudim/mc
