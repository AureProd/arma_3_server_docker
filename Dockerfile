FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/steamcmd:$PATH

RUN dpkg --add-architecture i386

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    ca-certificates \
    curl \
    lib32gcc-s1 \
    lib32stdc++6 \
    libsdl2-2.0-0 \
    lib32tinfo6 \
    lib32z1 \
    libtbb2:i386 \ 
    libtbb2 \
    liblzo2-2 \
    libvorbis0a \
    libvorbisfile3 \
    libvorbisenc2 \
    libogg0 \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY ./utils/depbo/lib /usr/local/lib
COPY ./utils/depbo/bin /usr/local/bin

RUN chmod +rwx /usr/local/lib/libdepbo.so.0*
RUN chmod +rwx /usr/local/bin/*

# Install depbo tools -> To use depbo makepbo -> makepbo -N <folder_to_pack>
RUN ldconfig

# Create steamcmd directory
WORKDIR /steamcmd

# Download and install SteamCMD -> To use steamcmd -> /steamcmd/steamcmd.sh
RUN curl -sSL https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz | tar -xzv -C /steamcmd

WORKDIR /utils/extdb3

COPY ./utils/extdb3 .

WORKDIR /builder

COPY ./builder .

RUN pip install /builder

WORKDIR /server

CMD ["python3", "-m", "builder", "-d"]