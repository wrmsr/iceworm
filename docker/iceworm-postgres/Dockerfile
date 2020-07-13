FROM postgres:12.3
COPY .dockertimestamp /

RUN ( \
  apt-get -o Acquire::Check-Valid-Until=false update && \
  apt-get install -y \
    apt-utils \
    build-essential \
    ca-certificates \
    curl \
    g++ \
    gcc \
    git-core \
    glib2.0 \
    iputils-ping \
    libc++-dev \
    libc++abi-dev \
    libtinfo5 \
    make \
    pkg-config \
    postgresql-server-dev-12 \
    procps \
    python \
    tmux \
    vim \
    wget \
)


RUN ( \
  export PLV8_VERSION=v2.3.15 && \
  mkdir -p /tmp/build && \
  cd /tmp/build && \
  curl -o "${PLV8_VERSION}.tar.gz" -SL "https://github.com/plv8/plv8/archive/${PLV8_VERSION}.tar.gz" && \
  tar xvzf "/tmp/build/${PLV8_VERSION}.tar.gz" -C /tmp/build/ && \
  cd "plv8-${PLV8_VERSION#?}" && \
  make && \
  make install \
)


COPY docker/omnibus-postgres/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
