FROM debian:sid

RUN apt-get update
RUN apt install -y -q \
    python3 \
    python3-pip \
    libelf-dev \
    bc \
    tree

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /app
WORKDIR /app

# Install nbuild
ADD . /app

# Some nice aliases
RUN echo "alias ls='ls --color'\nalias la='ls -la'" >> /root/.bashrc

# Manifests (entry)
VOLUME /app/manifests

# Packages (output)
VOLUME /app/packages

CMD bash
