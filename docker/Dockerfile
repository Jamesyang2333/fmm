FROM ubuntu:16.04
RUN apt-get update && apt-get install -y \
    build-essential software-properties-common\
    libboost-dev libboost-serialization-dev \
    cmake \
    make libbz2-dev libexpat1-dev swig python-dev
RUN add-apt-repository -y ppa:ubuntugis/ppa && apt-get -q update
RUN apt-get -y install gdal-bin libgdal-dev python-pip
RUN mkdir -p /fmm
COPY . /fmm
WORKDIR /fmm
RUN rm -rf build
RUN mkdir -p build && \
    cd build && \
    cmake .. && \
    make install
EXPOSE 1235
ENV PATH /fmm/build:$PATH
ENV PYTHONPATH /fmm/build/python:$PYTHONPATH
RUN python -m pip install tornado==5.1.1
RUN python -m pip install flask
RUN python -m pip install numpy==1.8.0
RUN cd /fmm/example/osm_example && python ubodt_data_gen.py
CMD cd /fmm/example/socket && python server.py -c fmm_config.json -p 1235
