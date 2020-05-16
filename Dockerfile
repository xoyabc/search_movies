FROM ubuntu

MAINTAINER xoyabc <lxh1031138448@gmail.com>

RUN apt-get update; \
    apt-get -y upgrade

RUN apt-get -y install g++ git

RUN mkdir /home/git; \
    cd /home/git; \
    sudo git clone https://github.com/xoyabc/search_movies.git -b master;
