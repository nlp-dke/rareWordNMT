#!/bin/bash

if [ -z "$BASEDIR" ]; then
    BASEDIR=/
fi

mkdir -p $BASEDIR/tmp/corpus
cd $BASEDIR/tmp/corpus
mkdir $BASEDIR/data/orig/dict/

wget https://dumps.wikimedia.org/enwiktionary/20200501/enwiktionary-20200501-pages-articles.xml.bz2
#https://github.com/tatuylonen/wiktextract
wiktwords enwiktionary-20200501-pages-articles.xml.bz2 --out en.wiktionary.words --language English --translations
sed -e "s/: true/: True/g" -e "s/: false/: False/g" en.wiktionary.words > en.wiktionary.words.mod
python3 $RARENMTDIR/scripts/dataCollection/Wiktionary.py --wiktionary en.wiktionary.words.mod --out en.wiktionary --target_language $tl
cp en.wiktionary.s  en.wiktionary.t $BASEDIR/data/orig/dict/
cd $BASEDIR
rm -r $BASEDIR/tmp/corpus/

