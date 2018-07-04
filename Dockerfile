FROM debian

RUN useradd -s /bin/bash nbuild

RUN apt-get update && apt-get install -y \
    bison \
    gawk \
    gcc \
    g++ \
    m4 \
    make \
    patch \
    perl \
    sed \
    tar \
    xz-utils \
    texinfo \
    python3 \
    python3-pip

ADD . /nbuild
WORKDIR /nbuild

RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED yes

VOLUME /build
VOLUME /packages
VOLUME /manifests

USER nbuild

ENTRYPOINT ["/nbuild/nbuild.py", "--build-dir=/build", "--pkg-dir=/packages"]
