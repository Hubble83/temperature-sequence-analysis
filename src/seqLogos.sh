#!/bin/bash

cd ../outputs/seqLogos
for file in fasta/*
do
	filename=$(basename "$file")
	filename=${filename%.*}

	echo $filename
	if [[ $filename == 4_* ]]
	then
		echo -e "\tDNA"
		python3 ../../src/weblogo/weblogo -c classic -n 50 < fasta/$filename.fasta > eps/$filename.eps
	else
		echo -e "\tProtein"
		python3 ../../src/weblogo/weblogo -c chemistry -n 50 < fasta/$filename.fasta > eps/$filename.eps
	fi
	convert -flatten -density 500 eps/$filename.eps  png/$filename.png
done