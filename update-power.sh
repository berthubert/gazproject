#!/bin/sh
rsync index-nl.html 10.0.0.4:/var/www/berthub.eu/html/nlelec/index.html
rsync *.svg 10.0.0.4:/var/www/berthub.eu/html/nlelec/
