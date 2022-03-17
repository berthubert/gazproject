#!/bin/sh

STARTDATE="2022-01-01"
ENDDATE="2022-03-15"
#ENDDATE=$(date +%Y-%m-%d)

wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=ua-tso-0001itp-00117exit&timezone=CET&to=${ENDDATE}" \
	-O uzhgorod.json
	
jq .operationalData < uzhgorod.json   > publish/uzhgorod-data.json


wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=de-tso-0018itp-00297entry&timezone=CET&to=${ENDDATE}" \
	-O nordstream-fluxsys.json

jq .operationalData < nordstream-fluxsys.json   > publish/nordstream-fluxsys-data.json

wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=de-tso-0016itp-00251entry&timezone=CET&to=${ENDDATE}" \
	-O nordstream-opal.json
	
jq .operationalData < nordstream-opal.json   > publish/nordstream-opal-data.json	


wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=pl-tso-0001itp-00104entry&timezone=CET&to=${ENDDATE}" \
	-O yamal-kondratki.json
	
jq .operationalData < yamal-kondratki.json   > publish/yamal-kondratki-data.json	


wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=pl-tso-0002itp-00092entry&timezone=CET&to=${ENDDATE}" \
	-O yamal-wysokoje.json
	
jq .operationalData < yamal-wysokoje.json   > publish/yamal-wysokoje-data.json	
	

wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=ua-tso-0001itp-10008exit&timezone=CET&to=${ENDDATE}" \
	-O hermanowice.json
	
jq .operationalData < hermanowice.json   > publish/hermanowice-data.json	
	
