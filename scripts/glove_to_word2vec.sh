#!/usr/bin/env bash
#Use this script to convert glove format vector files to word2vec format files
#Usage: ./glove_to_word2ved.sh input_file output_file

INPUT_FILE=$1
OUTPUT_FILE=$2
DIM=`awk -F " " "{print NF - 1; exit}" $INPUT_FILE`
WORDS=`wc -l $INPUT_FILE | cut -f3 -d" "`
echo $WORDS $DIM > $OUTPUT_FILE
cat $INPUT_FILE >> $OUTPUT_FILE