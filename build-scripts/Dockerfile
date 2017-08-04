FROM python

RUN apt-get -y update && \
    apt-get -y install sudo

ARG USER_UID
ARG USER_GID

RUN groupadd \
        --gid $USER_GID hostuser && \
    adduser \
        --uid $USER_UID \
        --gid $USER_GID \
        --disabled-password \
        --gecos "" hostuser && \
    usermod -aG sudo hostuser && \
    echo "hostuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

ADD build-scripts/build-requirements.txt /build/

ADD *requirements.txt /build/
RUN find /build -name '*requirements.txt' -exec pip install -r {} \;

USER hostuser