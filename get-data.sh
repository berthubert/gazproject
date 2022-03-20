#!/bin/sh

STARTDATE="2022-01-01"
ENDDATE="2022-03-19"
#ENDDATE=$(date +%Y-%m-%d)


#                                             ua-tso-0001itp-00117exit
#https://transparency.entsog.eu/api/v1/operationalData?from=2022-02-15&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=sk-tso-0001itp-00117entry&timezone=CET&to=2022-03-16

wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=bg-tso-0001itp-00549entry&timezone=CET&to=${ENDDATE}" \
	-O strandzha2.json
	
jq .operationalData < strandzha2.json   > strandzha2-data.json


wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=sk-tso-0001itp-00117entry&timezone=CET&to=${ENDDATE}" \
	-O uzhgorod.json
	
jq .operationalData < uzhgorod.json   > uzhgorod-data.json


wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=de-tso-0018itp-00297entry&timezone=CET&to=${ENDDATE}" \
	-O nordstream-fluxsys.json

jq .operationalData < nordstream-fluxsys.json   > nordstream-fluxsys-data.json

wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=de-tso-0016itp-00251entry&timezone=CET&to=${ENDDATE}" \
	-O nordstream-opal.json
	
jq .operationalData < nordstream-opal.json   > nordstream-opal-data.json	


wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=pl-tso-0001itp-00104entry&timezone=CET&to=${ENDDATE}" \
	-O yamal-kondratki.json
	
jq .operationalData < yamal-kondratki.json   > yamal-kondratki-data.json	


wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=pl-tso-0002itp-00092entry&timezone=CET&to=${ENDDATE}" \
	-O yamal-wysokoje.json
	
jq .operationalData < yamal-wysokoje.json   > yamal-wysokoje-data.json	
	
wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=day&periodize=0&pointDirection=ua-tso-0001itp-10008exit&timezone=CET&to=${ENDDATE}" \
	-O hermanowice.json
	
jq .operationalData < hermanowice.json   > hermanowice-data.json	


