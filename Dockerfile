FROM ravenos/raven-os

RUN yes | nest pull
RUN yes | nest install essentials-dev

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /app
WORKDIR /app

# Install nbuild
ADD . /app
ADD config.toml.example /app/config.toml

# Manifests (entry)
VOLUME /app/manifests

# Packages (output)
VOLUME /app/packages

CMD bash
