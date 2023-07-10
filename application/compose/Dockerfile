# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 ubuntu:22.04
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=1
ENV DEBIAN_FRONTEND="noninteractive"
ENV OPENCV_LOG_LEVEL=DEBUG
ENV OPENCV_VIDEOIO_DEBIG=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential \
    && apt-get install --no-install-recommends -y python3 python3-pip python3-dev

RUN apt-get install -y build-essential cmake git pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-dev libopenexr-dev \
    libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev

RUN mkdir ~/opencv_build && cd ~/opencv_build \
    && git clone https://github.com/opencv/opencv.git \
    && git clone https://github.com/opencv/opencv_contrib.git \
    && cd ~/opencv_build/opencv && git checkout 4.7.0 \
    && cd ~/opencv_build/opencv_contrib && git checkout 4.7.0

#ENV LD_LIBRARY_PATH=$FFMPEG_PATH/lib/:$LD_LIBRARY_PATH
#ENV PKG_CONFIG_PATH=$FFMPEG_PATH/lib/pkgconfig:$PKG_CONFIG_PATH

RUN cd ~/opencv_build/opencv \
    && git checkout 4.7.0 \
    && mkdir build && cd build \
    && cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_opencv_python2=OFF \
    -D BUILD_opencv_contrib=OFF \
    -D BUILD_JAVA=OFF \
    -D BUILD_FAT_JAVA_LIB=OFF \
    -D BUILD_TESTS=OFF \
    -D ENABLE_PYLINT=OFF \
    -D ENABLE_FLAKE8=OFF \
    -D WITH_TBB=ON \
    -D BUILD_TBB=ON \
    -D OPENCV_DUMP_HOOKS_FLOW=ON \
    -D WITH_V4L=ON \
    -D WITH_FFMPEG=ON ..

RUN cd ~/opencv_build/opencv/build \
    && make -j24

RUN  cd ~/opencv_build/opencv/build \
    && make install

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY . /app

COPY ./compose/start /start
RUN sed -i 's/\r$//g' /start \
    && chmod +x /start
WORKDIR /app

EXPOSE 8000

CMD ["/start"]