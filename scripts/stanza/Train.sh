#!/bin/bash

if [ -z "$BASEDIR" ]; then
    BASEDIR=/
fi
if [ -z "$RARENMTDIR" ]; then
    NMTDIR=/opt/SLT.KIT/
fi

if [ -z "$POS" ]; then
    POS=""
fi


input=$1
name=$2
echo $POS

mkdir -p $BASEDIR/model/${name}
mkdir -p $BASEDIR/data/${name}/train
mkdir -p $BASEDIR/data/${name}/valid
mkdir -p $BASEDIR/data/${name}/dict

for f in $BASEDIR/data/${input}/parallel/*\.s
do
python3 $RARENMTDIR/scripts/stanza/ApplyStanza.py --input $f --lang $sl --output $BASEDIR/data/${name}/train/${f##*/} $POS
done

for f in $BASEDIR/data/${input}/parallel/*\.t
do
python3 $RARENMTDIR/scripts/stanza/ApplyStanza.py --input $f --lang $tl --output $BASEDIR/data/${name}/train/${f##*/} $POS
done

dir=dict
for dir in valid dict
do
for f in `ls $BASEDIR/data/${input}/$dir/*\.s`
do
echo $f
python3 $RARENMTDIR/scripts/stanza/ApplyStanza.py --input $f --lang $sl --output $BASEDIR/data/${name}/$dir/${f##*/} $POS
done
done

for dir in valid dict
do
for f in `ls $BASEDIR/data/${input}/$dir/*\.t`
do
echo $f
python3 $RARENMTDIR/scripts/stanza/ApplyStanza.py --input $f --lang $tl --output $BASEDIR/data/${name}/$dir/${f##*/} $POS
done
done


