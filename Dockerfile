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

ADD /build-requirements.txt /build/build-requirements.txt
RUN pip install -r /build/build-requirements.txt

USER hostuser