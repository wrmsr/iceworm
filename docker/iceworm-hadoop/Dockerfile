FROM ubuntu:eoan-20200410
COPY .dockertimestamp /


# Packages

RUN ( \
  apt-get -o Acquire::Check-Valid-Until=false update && \
  DEBIAN_FRONTEND="noninteractive" apt-get install -y \
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
    procps \
    python \
    software-properties-common \
    tmux \
    vim \
    wget \
)


# JDK

RUN ( \
    add-apt-repository ppa:openjdk-r/ppa && \
    apt-get update && \
    apt-get install -y openjdk-8-jdk \
)

RUN ( \
    # https://stackoverflow.com/questions/6784463/error-trustanchors-parameter-must-be-non-empty \
    /usr/bin/printf '\xfe\xed\xfe\xed\x00\x00\x00\x02\x00\x00\x00\x00\xe2\x68\x6e\x45\xfb\x43\xdf\xa4\xd9\x92\xdd\x41\xce\xb6\xb2\x1c\x63\x30\xd7\x92' > /etc/ssl/certs/java/cacerts && \
    /var/lib/dpkg/info/ca-certificates-java.postinst configure \
)


# Install

RUN mkdir /opt/hadoop
WORKDIR /opt/hadoop
RUN wget "http://mirrors.ibiblio.org/apache/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz"
RUN tar xvzf hadoop-3.2.1.tar.gz

RUN ( \
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys \
)
RUN apt-get install -y openssh-server
RUN sed -i 's/\(#\)\{0,1\}PermitRootLogin .*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN mkdir -p /run/sshd

COPY docker/iceworm-hadoop/hadoop-env.sh hadoop-3.2.1/etc/hadoop/
COPY docker/iceworm-hadoop/core-site.xml hadoop-3.2.1/etc/hadoop/
COPY docker/iceworm-hadoop/hdfs-site.xml hadoop-3.2.1/etc/hadoop/

RUN hadoop-3.2.1/bin/hdfs namenode -format
RUN ( \
  ((/usr/sbin/sshd -D -o ListenAddress=0.0.0.0) &) && sleep 3 && \
  cd hadoop-3.2.1 && \
  sbin/start-dfs.sh && \
  bin/hdfs dfs -mkdir /user && \
  bin/hdfs dfs -mkdir /user/root && \
  bin/hdfs dfs -mkdir input && \
  bin/hdfs dfs -put etc/hadoop/*.xml input && \
  bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar grep input output 'dfs[a-z.]+' && \
  bin/hdfs dfs -get output output && \
  cat output/* && \
  bin/hdfs dfs -cat output/* && \
  sbin/stop-dfs.sh \
)

COPY docker/iceworm-hadoop/mapred-site.xml hadoop-3.2.1/etc/hadoop/
COPY docker/iceworm-hadoop/yarn-site.xml hadoop-3.2.1/etc/hadoop/
RUN ( \
  ((/usr/sbin/sshd -D -o ListenAddress=0.0.0.0) &) && sleep 3 &\
  cd hadoop-3.2.1 && \
  sbin/start-dfs.sh && \
  sbin/start-yarn.sh && \
  sleep 5 && \
  sbin/stop-yarn.sh && \
  sbin/stop-dfs.sh \
)

RUN apt-get install -y htop sudo
RUN ( \
  wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
  sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list' && \
  apt-get update && \
  apt-get install -y postgresql postgresql-contrib \
)
RUN ( \
  ((pg_ctlcluster 12 main start) &) && sleep 3 && \
  sudo -upostgres createdb iceworm && \
  sudo -upostgres psql -c 'select 1' \
)
