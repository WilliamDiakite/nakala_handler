#!/bin/bash

echo "Enter packets folder location [press enter for "input"]:"
read INPUT_FOLDER
if [ "$INPUT_FOLDER" = "" ]; then
    INPUT_FOLDER="input"
fi

echo "Enter output folder location [press enter for "output"]:"
read OUTPUT_FOLDER
if [ "$OUTPUT_FOLDER" = "" ]; then
    OUTPUT_FOLDER="output"
fi

echo "Enter project handle [Leave empty if only one project]:"
read projectId
projectIdParam="-projectId"
if [ "$projectId" = "" ]; then
    projectIdParam=""
fi

while true; do
    echo "Clean output folder (y/n) (WARNING : this will delete files in output folder) ? [press enter for "n"]"
    read CLEANOUTPUT
    if [ "$CLEANOUTPUT" = "Y" -o "$CLEANOUTPUT" = "y" ]; then
        CLEANOUTPUT="-cleanOutput"
        break
    fi
    if [ "$CLEANOUTPUT" = "N" -o "$CLEANOUTPUT" = "n" -o "$CLEANOUTPUT" = "" ]; then
        CLEANOUTPUT=""
        break
    fi
done

while true; do
    echo "Include facile validation on server (y/n) ? [press enter for "n"]"
    read FACILE
    if [ "$FACILE" = "Y" -o "$FACILE" = "y" ]; then
        FACILE="-facileValidation"
        break
    fi
    if [ "$FACILE" = "N" -o "$FACILE" = "n" -o "$FACILE" = "" ]; then
        FACILE=""
        break
    fi
done

while true; do
    echo "Replace metadata or data+metadata (y/n) ? [press enter for "n"]"
    read REPLACE
    if [ "$REPLACE" = "Y" -o "$REPLACE" = "y" ]; then
        REPLACE="-replace"
        break
    fi
    if [ "$REPLACE" = "N" -o "$REPLACE" = "n" -o "$REPLACE" = "" ]; then
        REPLACE=""
        break
    fi
done

if [ "$REPLACE" = "" ]; then
    while true; do
        echo "Update data files only (y/n) ? [press enter for "n"]"
        read UPDATEDATA_ONLY
        if [ "$UPDATEDATA_ONLY" = "Y" -o "$UPDATEDATA_ONLY" = "y" ]; then
            UPDATEDATA_ONLY="-updateDataOnly"
            break
        fi
        if [ "$UPDATEDATA_ONLY" = "N" -o "$UPDATEDATA_ONLY" = "n" -o "$UPDATEDATA_ONLY" = "" ]; then
            UPDATEDATA_ONLY=""
            break
        fi
    done
fi

while true; do
    echo "Enter email address:"
    read EMAIL
    if [ "$EMAIL" != "" ]; then
		break
    fi
done

echo "Enter api key file location [press enter for 'nakala-key.txt']:"
read apiKeyFile
if [ "$apiKeyFile" = "" ]; then
    apiKeyFile="nakala-key.txt"
fi


java --add-modules=java.xml.bind -XX:+IgnoreUnrecognizedVMOptions -jar nakala-console.jar -email $EMAIL -inputFolder $INPUT_FOLDER -outputFolder $OUTPUT_FOLDER $projectIdParam $projectId -apiKeyFile $apiKeyFile $FACILE $CLEANOUTPUT $REPLACE $UPDATEDATA_ONLY

read -p "Press [Enter] key to continue..."