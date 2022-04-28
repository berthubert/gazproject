#!/bin/bash
curl 'https://agsi.gie.eu/api?continent=EU&from=2022-01-01&to=2022-05-01&page=1&size=365'  --fail > storage-tmp.json && jq .data < storage-tmp.json > storage-data3.json
