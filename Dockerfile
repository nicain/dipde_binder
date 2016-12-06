FROM andrewosh/binder-base

MAINTAINER Nicholas Cain <nicholasc@galleninstitute.org>

ARG DIPDE_BRANCH=dipde_binder

USER root

RUN apt-get update
#RUN apt-get install -y xvfb

USER main

RUN pip install https://github.com/nicain/dipde_dev/zipball/$DIPDE_BRANCH
#RUN /usr/bin/xvfb-run py.test /home/main/anaconda2/lib/python2.7/site-packages/dipde/test 2> /dev/null
#RUN py.test /home/main/anaconda2/lib/python2.7/site-packages/dipde/test
