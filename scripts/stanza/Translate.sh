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

set=$1
input=$2
name=$3


mkdir -p $BASEDIR/data/${name}/eval

xml=0
if [ -f $BASEDIR/data/orig/eval/$set/IWSLT.$set/IWSLT.TED.$set.$sl-$tl.$sl.xml ]; then
    inFile=$BASEDIR/data/orig/eval/$set/IWSLT.$set/IWSLT.TED.$set.$sl-$tl.$sl.xml
    tinFile=$BASEDIR/data/orig/eval/$set/IWSLT.$set/IWSLT.TED.$set.$sl-$tl.$tl.xml
    xml=1
elif [ -f $BASEDIR/data/orig/eval/$set/$set.$sl ]; then
    inFile=$BASEDIR/data/orig/eval/$set/$set.$sl
    tinFile=$BASEDIR/data/orig/eval/$set/$set.$tl
    xml=0
fi

xmlcommand=""
if [ $xml -eq 1 ]; then
    cat $inFile | grep "<seg id" | sed -e "s/<[^>]*>//g"  > $BASEDIR/data/${name}/eval/$set.s.temp
    python3 $RARENMTDIR/scripts/stanza/ApplyStanza.py --input $BASEDIR/data/${name}/eval/$set.s.temp --lang $sl --output $BASEDIR/data/${name}/eval/$set.s $POS
    rm $BASEDIR/data/${name}/eval/$set.s.temp

    cat $tinFile | grep "<seg id" | sed -e "s/<[^>]*>//g"  > $BASEDIR/data/${name}/eval/$set.t.temp
    python3 $RARENMTDIR/scripts/stanza/ApplyStanza.py --input $BASEDIR/data/${name}/eval/$set.t.temp --lang $tl --output $BASEDIR/data/${name}/eval/$set.t $POS
    rm $BASEDIR/data/${name}/eval/$set.t.temp

else
    python3 $RARENMTDIR/scripts/stanza/ApplyStanza.py --input $inFile --lang $sl --output $BASEDIR/data/${name}/eval/$set.s $POS
    python3 $RARENMTDIR/scripts/stanza/ApplyStanza.py --input $tinFile --lang $tl --output $BASEDIR/data/${name}/eval/$set.t $POS
     
fi

