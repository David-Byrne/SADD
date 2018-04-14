FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y libgmp10 \
                                         wget \
                                         texlive \
                                         texlive-latex-base \
                                         texlive-latex-recommended \
                                         texlive-xetex

RUN wget https://github.com/jgm/pandoc/releases/download/2.1.3/pandoc-2.1.3-1-amd64.deb

RUN dpkg -i pandoc-2.1.3-1-amd64.deb

