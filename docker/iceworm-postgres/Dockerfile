FROM postgres:9.6.17
COPY .dockertimestamp /

RUN ( \
  sed -i "s/.*jessie-updates.*/deb [check-valid-until=no] http:\/\/archive.debian.org\/debian jessie-backports main/" /etc/apt/sources.list && \
  apt-get -o Acquire::Check-Valid-Until=false update && \
  apt-get install -y \
    apt-utils \
    build-essential \
    ca-certificates \
    curl \
    gcc \
    git-core \
    iputils-ping \
    postgresql-server-dev-9.6 \
    python \
    vim \
)

ENV \
  PLV8_VERSION=v2.1.0 \
  PLV8_SHASUM="207d712e919ab666936f42b29ff3eae413736b70745f5bfeb2d0910f0c017a5c  v2.1.0.tar.gz"

RUN ( \
  mkdir -p /tmp/build && \
  curl -o /tmp/build/${PLV8_VERSION}.tar.gz -SL "https://github.com/plv8/plv8/archive/$PLV8_VERSION.tar.gz" && \
  cd /tmp/build && \
  echo ${PLV8_SHASUM} | sha256sum -c && \
  tar -xzf /tmp/build/${PLV8_VERSION}.tar.gz -C /tmp/build/ && \
  cd /tmp/build/plv8-${PLV8_VERSION#?} && \
  sed -i 's/\(depot_tools.git\)/\1; cd depot_tools; git checkout 46541b4996f25b706146148331b9613c8a787e7e; rm -rf .git;/' Makefile.v8 && \
  make -j static && \
  make install \
)
