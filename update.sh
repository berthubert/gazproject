#!/bin/bash
# ./get-storage.sh
./get-data.sh
python3 gazmon.py
rsync index.html *.png  10.0.0.4:/var/www/berthub.eu/html/gazmon

