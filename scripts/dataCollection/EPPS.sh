#!/bin/bash


if [ -z "$BASEDIR" ]; then
    BASEDIR=/
fi

mkdir -p $BASEDIR/tmp/corpus
cd $BASEDIR/tmp/corpus

mkdir -p $BASEDIR/data/orig/parallel/

if [ $sl == "en" ]; then
    wget http://statmt.org/europarl/v7/$tl-$sl.tgz
    tar -xzvf ${tl}-${sl}.tgz
    cp $BASEDIR/tmp/corpus/europarl-v7.$tl-$sl.$sl $BASEDIR/data/orig/parallel/EPPS.s
    cp $BASEDIR/tmp/corpus/europarl-v7.$tl-$sl.$tl $BASEDIR/data/orig/parallel/EPPS.t
else
    wget http://statmt.org/europarl/v7/$sl-$tl.tgz
    tar -xzvf ${sl}-${tl}.tgz
    cp $BASEDIR/tmp/corpus/europarl-v7.$sl-$tl.$sl $BASEDIR/data/orig/parallel/EPPS.s
    cp $BASEDIR/tmp/corpus/europarl-v7.$sl-$tl.$tl $BASEDIR/data/orig/parallel/EPPS.t
fi




rm -r $BASEDIR/tmp/corpus/
