#!/bin/bash


source ../Config.sh


export systemName=TED
export sl=en
export tl=de


export BASEDIR=$DICTDIR/ted/
export BPESIZE=10000

export LAYER=12
export TRANSFORMER=transformer

mkdir -p $BASEDIR
echo $BASEDIR


##############   DOWNLOAD Data   #############################
$RARENMTDIR/scripts/dataCollection/IWSLT.2017.sh 
$RARENMTDIR/scripts/dataCollection/Wiktionary.sh

export POS="--pos"
$RARENMTDIR/scripts/stanza/Train.sh orig prepro

$RARENMTDIR/scripts/dataSplit/Split.sh TED
