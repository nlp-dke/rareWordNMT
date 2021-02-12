#!/bin/bash


source ../Config.sh


export systemName=Europarl
export sl=en
export tl=de


export BASEDIR=$DICTDIR/europarl.de/
export BPESIZE=10000

export LAYER=12
export TRANSFORMER=transformer

mkdir -p $BASEDIR
echo $BASEDIR


##############   DOWNLOAD Data   #############################
$RARENMTDIR/scripts/dataCollection/EPPS.sh 
$RARENMTDIR/scripts/dataCollection/Wiktionary.sh

$RARENMTDIR/scripts/stanza/Train.sh orig prepro

$RARENMTDIR/scripts/dataSplit/Split.sh TED
