# Starting with a Ubuntu docker file
FROM ubuntu:rolling
ENV DEBIAN_FRONTEND=noninteractive 
LABEL maintainer="Orhan Ermis <ermis@eurecom.fr>"
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
# Updating
RUN apt-get update -q -y

# Installing dependencies
RUN apt-get install -q -y make
RUN apt-get install -q -y g++-8
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 20
RUN apt-get install -q -y cmake
RUN apt-get install -q -y libgmp-dev
RUN apt-get install -q -y libssl-dev
RUN apt-get install -q -y libboost-all-dev
RUN apt-get install -q -y tmux
RUN apt-get install -q -y wget
RUN apt-get install -q -y git
RUN wget -c 'http://sourceforge.net/projects/boost/files/boost/1.66.0/boost_1_66_0.tar.bz2'
RUN tar xf boost_1_66_0.tar.bz2
RUN cd boost_1_66_0/ && ./bootstrap.sh --prefix=/usr/local/ && ./b2 && ./b2 install
RUN ldconfig
RUN wget https://cmake.org/files/v3.12/cmake-3.12.4.tar.gz
RUN tar -xzvf cmake-3.12.4.tar.gz
RUN cd cmake-3.12.4 && ./bootstrap && make -j4 && make install
RUN apt-get install -q -y curl
RUN apt-get install -q -y unzip
#FROM python:3
RUN mkdir app
COPY ABY.zip /app 
WORKDIR /app
RUN unzip ABY.zip
RUN cd ABY/ && mkdir build 
RUN ls ABY/
RUN cd ABY/build/ && cmake .. 
RUN cd ABY/build/ && make 
RUN cd ABY/build/ && make install
COPY requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN apt-get update -y
RUN apt-get install -q -y python3-sklearn
COPY . /app 
RUN cd 2pc_model_quantized_batches/ && make WITH_MAX=1
ENTRYPOINT ["python3"]
CMD ["app.py"]