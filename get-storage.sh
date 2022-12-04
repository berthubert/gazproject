#!/bin/bash
#curl 'https://agsi.gie.eu/api?continent=EU&from=2022-01-01&to=2022-06-22&page=1&size=365'  --fail > storage-tmp.json && jq .data < storage-tmp.json > storage-data3.json


curl 'https://agsi.gie.eu/api?continent=EU&from=2019-11-20&to=2022-01-01&page=1&size=7000' \
  -H 'authority: agsi.gie.eu' \
  -H 'accept: application/json' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
 -H 'pragma: no-cache' \
  --header "x-key: $(cat gie.key)" \
  -H 'referer: https://agsi.gie.eu/historical/eu' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' \
  --compressed --fail > storage-tmp.json && jq .data < storage-tmp.json > storage-old.json
  
  
 curl 'https://agsi.gie.eu/api?continent=EU&from=2022-01-01&to=2023-01-01&page=1&size=7000' \
  -H 'authority: agsi.gie.eu' \
  -H 'accept: application/json' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
 -H 'pragma: no-cache' \
  --header "x-key: $(cat gie.key)" \
  -H 'referer: https://agsi.gie.eu/historical/eu' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' \
  --compressed --fail > storage-tmp.json && jq .data < storage-tmp.json > storage-new.json
  