#!/bin/bash
./get-data-intraday.sh
python3 gazmon.py
rsync index.html livegraph.png livegraph.svg 10.0.0.4:/var/www/berthub.eu/html/gazmon

