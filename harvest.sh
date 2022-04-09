#!/bin/bash

NUM=0
while [ "$NUM" != "6" ]
do 
	NUM=$(ls -1 chrome/*.csv | wc -l)
	echo $NUM
	sleep 1
done


for a in chrome/Cross*.csv 
do
	echo -n "$a: "
	head -1 "$a"
	newname=$(head -1 "$a" | cut -f2 -d\| | cut -f1 -d" " | tr "A-Z" "a-z")
	newdate=$(echo "$a" | cut -f2 -d_ | cut -b1-8)
	cp "$a" harvested/nl$newname-$newdate.csv
done

for a in chrome/Actual*csv # Actual Generation per Production Type_202204020000-202204030000.csv'
do 
	echo -n "$a: "
	head -1 "$a"
	newdate=$(echo "$a" | cut -f2 -d_ | cut -b1-8)
	cp "$a" harvested/nlprod-$newdate.csv
done
