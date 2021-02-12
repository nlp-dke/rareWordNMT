#!/bin/bash


corpus=$1

##############   SPLITDATA   #############################


dict=en.wiktionary
cd $BASEDIR/data/prepro/dict/

python3 $RARENMTDIR/scripts/dict/MarkeAmbigous.py --source_dict $dict.s.lemma --target_dict $dict.t.lemma > $dict.selected

for suffix in s s.lemma t t.lemma
do
paste $dict.selected $dict.$suffix | awk -F '\t' '{if($1 == 1) print $2}' > $dict.filtered.$suffix
done



python3 $RARENMTDIR/scripts/dict/CalcStatsitics.py  --source_dict $dict.filtered.s.lemma --target_dict $dict.filtered.t.lemma --source_corpus ../train/$corpus.s --target_corpus ../train/$corpus.t > $dict.filtered.stats
python3 $RARENMTDIR/scripts/dict/CalcStatsitics.py  --source_dict $dict.filtered.t.lemma --target_dict $dict.filtered.s.lemma --source_corpus ../train/$corpus.t --target_corpus ../train/$corpus.s > $dict.filtered.inv_stats
cut -d "#" -f 1-6 $dict.filtered.stats | paste - $dict.filtered.inv_stats -d '#' | sort -g -k 1,1 -t "#" > $dict.entries

awk -F '#' '{if($1 > 3 && $1 < 80 && $6 > 1 && $5 < 10 && $11 < 10) print;}' $dict.entries > $dict.selectedEntries
wc $dict.selectedEntries
awk -F '#' '{print $14,"#",$13}' $dict.selectedEntries | sort -u > $dict.selectedEntries.uniq
awk -F '#' '{print $1}' $dict.selectedEntries.uniq > $dict.selectedEntries.s
awk -F '#' '{print $2}' $dict.selectedEntries.uniq > $dict.selectedEntries.t

awk '{if (NR%3 == 1) {print "TEST"}else if (NR%3 == 2) {print "MIX"} else{print "TRAIN"}}' $dict.selectedEntries.t  > $dict.selectedEntries.subset.temp


python3 $RARENMTDIR/scripts/dict/SplitData.py  --source_dict $dict.selectedEntries.s --target_dict $dict.selectedEntries.t --split $dict.selectedEntries.subset.temp --source_corpus ../train/$corpus.s --target_corpus ../train/$corpus.t > $dict.sentenceSelection
awk -F '#' '{print $2}' $dict.sentenceSelection > $dict.sentenceAnnotation
python3 $RARENMTDIR/scripts/dict/ClassifyDictionary.py --source_dict $dict.selectedEntries.s --target_dict $dict.selectedEntries.t --sentenceAnnotation $dict.sentenceSelection  > $dict.selectedEntries.subset



mkdir -p $BASEDIR/data/newsplit/train
mkdir -p $BASEDIR/data/newsplit/valid
mkdir -p $BASEDIR/data/newsplit/eval
mkdir -p $BASEDIR/data/newsplit/dict

cp $dict.selectedEntries.s $dict.selectedEntries.t $dict.selectedEntries.subset $BASEDIR/data/newsplit/dict


for suffix in s t s.lemma t.lemma s.pos t.pos
do
awk '{print $1}' $dict.sentenceSelection | paste - ../train/$corpus.$suffix | awk -F ' ' '{if($1 == "TRAIN") print $0}' | cut -d $'\t' -f 2- > $BASEDIR/data/newsplit/train/$corpus.$suffix
awk '{print $1}' $dict.sentenceSelection | paste - ../train/$corpus.$suffix | awk -F ' ' '{if($1 == "VALID") print $0}' | cut -d $'\t' -f 2- > $BASEDIR/data/newsplit/valid/valid.$suffix
awk '{print $1}' $dict.sentenceSelection | paste - ../train/$corpus.$suffix | awk -F ' ' '{if($1 == "TEST") print $0}' | cut -d $'\t' -f 2- > $BASEDIR/data/newsplit/eval/test.$suffix
done
awk '{print $1}' $dict.sentenceSelection | paste - $dict.sentenceAnnotation | awk -F ' ' '{if($1 == "TRAIN") print $0}' | cut -d $'\t' -f 2- > $BASEDIR/data/newsplit/train/$corpus.annotation
awk '{print $1}' $dict.sentenceSelection | paste - $dict.sentenceAnnotation | awk -F ' ' '{if($1 == "VALID") print $0}' | cut -d $'\t' -f 2- > $BASEDIR/data/newsplit/valid/valid.annotation
awk '{print $1}' $dict.sentenceSelection | paste - $dict.sentenceAnnotation | awk -F ' ' '{if($1 == "TEST") print $0}' | cut -d $'\t' -f 2- > $BASEDIR/data/newsplit/eval/test.annotation

awk '{print $1}' $dict.sentenceSelection | paste - ../train/$corpus.s | awk -F ' ' '{if($1 == "TEST") print $0}' | cut -d $'\t' -f 2- > $BASEDIR/data/orig/eval/test.s
awk '{print $1}' $dict.sentenceSelection | paste - ../train/$corpus.t | awk -F ' ' '{if($1 == "TEST") print $0}' | cut -d $'\t' -f 2- > $BASEDIR/data/orig/eval/test.t

