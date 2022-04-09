#!/bin/bash
curl 'https://agsi.gie.eu/api?continent=EU&from=2022-03-01&to=2022-04-08&page=1&size=40'  --fail > storage-tmp.json && jq .data < storage-tmp.json > storage-data2.json