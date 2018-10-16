#!/bin/bash

# adjust email
# EMAIL="thomas.francart@sparna.fr"
EMAIL="nicolas.larrousse@huma-num.fr"

# adjust API key file.
API_KEY_FILE=nakala-key.txt

############## DO NOT MODIFY BEYOND THIS LINE ########################

if [ $# -eq 0 ]
  then
    echo "Usage : xxxxx.sh <paquet.zip>"
    echo "Don't forget to adjust email in the script and to save your API key in nakala-key.txt"
    exit 1
fi

INPUT_FILE=$1
INPUT_FILE_BASENAME=$(basename "$1")

# Adjust if necessary, but this should not be needed
INPUT_FOLDER="input-create-paquet"
OUTPUT_FOLDER="output-create-paquet"

# clean output folder. Set to "" to disable
CLEANOUTPUT="-cleanOutput"

# disable facile validation. Set to "-facileValidation" to enable
FACILE=""

# disable metadata+data replace. Set to "-replace" to enable
REPLACE=""

# disable data update. Set to "-updateDataOnly" to enable
UPDATEDATA_ONLY=""

# recreate input folder if needed
mkdir -p $INPUT_FOLDER
# recreate output folder if needed
mkdir -p $OUTPUT_FOLDER
# garantee output folder is cleaned
rm -rf $OUTPUT_FOLDER/*
# copy input file to input folder
cp $INPUT_FILE $INPUT_FOLDER

# clean the previous report
rm -rf report.xml
# clean the previous output metadata file
rm -rf $INPUT_FILE_BASENAME.xml

java --add-modules=java.xml.bind -XX:+IgnoreUnrecognizedVMOptions -jar nakala-console.jar -email $EMAIL -inputFolder $INPUT_FOLDER -outputFolder $OUTPUT_FOLDER $FACILE $CLEANOUTPUT $REPLACE $UPDATEDATA_ONLY -apiKeyFile $API_KEY_FILE

# extract the output from output folder
cp $OUTPUT_FOLDER/ok/*.xml .
cp $OUTPUT_FOLDER/report_*.xml report.xml

# clean input and output folder
rm -rf $INPUT_FOLDER
rm -rf $OUTPUT_FOLDER