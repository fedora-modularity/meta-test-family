FROM registry.fedoraproject.org/fedora:26
LABEL maintainer "Tomas Tomecek \"ttomecek@redhat.com\""

ENV NAME=tools VERSION=0 RELEASE=2 ARCH=x86_64
LABEL com.redhat.component="$NAME" \
      name="$FGC/$NAME" \
      version="$VERSION" \
      release="$RELEASE.$DISTTAG" \
      architecture="$ARCH" \
      run="docker run -it --name NAME --privileged --ipc=host --net=host --pid=host -e HOST=/host -e NAME=NAME -e IMAGE=IMAGE -v /run:/run -v /var/log:/var/log -v /etc/machine-id:/etc/machine-id -v /etc/localtime:/etc/localtime -v /:/host IMAGE" \
      summary="container with all the management tools you miss in Atomic Host"

# vim-minimal conflicts with vim-enhanced
RUN dnf remove -y vim-minimal && dnf install -y \
  bash-completion \
  bc \
  bind-utils \
  blktrace \
  crash \
  e2fsprogs \
  ethtool \
  file \
  gcc \
  gdb \
  git-core \
  glibc-utils \
  gomtree \
  htop \
  hwloc \
  iotop \
  iproute \
  iputils \
  less \
  ltrace \
  mailx \
  net-tools \
  netsniff-ng \
  nmap-ncat \
  numactl \
  numactl-devel \
  parted \
  pciutils \
  perf \
  procps-ng \
  psmisc \
  screen \
  sos \
  strace \
  sysstat \
  tcpdump \
  tmux \
  vim-enhanced \
  xfsprogs \
  && dnf clean all

# FIXME: current go-md2man can't convert tables :<
COPY ./root/ /

CMD ["/usr/bin/bash"]
