FROM ubuntu:focal-20200729
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
  sudo -upostgres psql -c "create user iceworm password 'iceworm'"  && \
  sudo -upostgres createdb iceworm && \
  sudo -upostgres psql -c 'select 1' && \
  pg_ctlcluster 12 main stop \
)

RUN wget "http://mirrors.advancedhosters.com/apache/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz"
RUN tar xzvf apache-hive-3.1.2-bin.tar.gz
# https://cwiki.apache.org/confluence/display/Hive/GettingStarted#GettingStarted-RunningHive
RUN ( \
  ((/usr/sbin/sshd -D -o ListenAddress=0.0.0.0) &) && sleep 3 && \
  ((pg_ctlcluster 12 main start) &) && sleep 3 && \
  hadoop-3.2.1/sbin/start-dfs.sh && \
  hadoop-3.2.1/sbin/start-yarn.sh && \
  sleep 5 && \
  (for i in $(seq 5) ; do hadoop-3.2.1/bin/hdfs dfsadmin -safemode get ; sleep 2 ; done) && \
  rm apache-hive-3.1.2-bin/lib/guava-19.0.jar && \
  cp hadoop-3.2.1/share/hadoop/hdfs/lib/guava-27.0-jre.jar apache-hive-3.1.2-bin/lib/ && \
  cd apache-hive-3.1.2-bin && \
  export HADOOP_HOME=/opt/hadoop/hadoop-3.2.1 && \
  $HADOOP_HOME/bin/hadoop fs -mkdir       /tmp && \
  $HADOOP_HOME/bin/hadoop fs -mkdir       /user/hive && \
  $HADOOP_HOME/bin/hadoop fs -mkdir       /user/hive/warehouse && \
  $HADOOP_HOME/bin/hadoop fs -chmod g+w   /tmp && \
  $HADOOP_HOME/bin/hadoop fs -chmod g+w   /user/hive/warehouse && \
  export HIVE_HOME=/opt/hadoop/apache-hive-3.1.2-bin && \
  export PATH="$HIVE_HOME/bin:$PATH" && \
  $HIVE_HOME/bin/schematool -dbType derby -initSchema && \
  cd .. && \
  hadoop-3.2.1/sbin/stop-dfs.sh && \
  hadoop-3.2.1/sbin/stop-yarn.sh \
)
