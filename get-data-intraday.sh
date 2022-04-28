#!/bin/bash

NOW=$(date +%s)


STARTDATE=$(date -d @$[$NOW - 2*86400] +%Y-%m-%d)
ENDDATE=$(date -d @$[$NOW + 86400] +%Y-%m-%d)

echo $STARTDATE
echo $ENDDATE


#https://transparency.entsog.eu/api/v1/operationalData.xlsx?forceDownload=true&pointDirection=tr-tso-0004itp-00549exit,bg-tso-0001itp-00549entry&from=2022-02-19&to=2022-03-18&indicator=Physical%20Flow&periodType=hour&timezone=CET&limit=-1&dataset=1&directDownload=true
# bg-tso-0001itp-00549entry


#                                             ua-tso-0001itp-00117exit
#https://transparency.entsog.eu/api/v1/operationalData?from=2022-02-15&indicator=Physical%20Flow&limit=-1&periodType=hour&periodize=0&pointDirection=sk-tso-0001itp-00117entry&timezone=CET&to=2022-03-16
# 

#wget "https://transparency.entsog.eu/api/v1/operationalData?pointDirection=bg-tso-0001itp-00549entry&from=${STARTDATE}&to=${ENDDATE}&indicator=Physical%20Flow&periodType=hour&timezone=UTC&limit=-1&dataset=1&directDownload=true" \

wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=hour&periodize=0&pointDirection=bg-tso-0001itp-00549entry&timezone=UTC&to=${ENDDATE}" \
	-O strandzha2-intraday.json && jq .operationalData < strandzha2-intraday.json   > strandzha2-data-intraday.json


wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=hour&periodize=0&pointDirection=sk-tso-0001itp-00117entry&timezone=UTC&to=${ENDDATE}" \
	-O uzhgorod-intraday.json && jq .operationalData < uzhgorod-intraday.json   > uzhgorod-data-intraday.json


wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=hour&periodize=0&pointDirection=de-tso-0018itp-00297entry&timezone=UTC&to=${ENDDATE}" \
	-O nordstream-fluxsys-intraday.json && jq .operationalData < nordstream-fluxsys-intraday.json   > nordstream-fluxsys-data-intraday.json

wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=hour&periodize=0&pointDirection=de-tso-0016itp-00251entry&timezone=UTC&to=${ENDDATE}" \
	-O nordstream-opal-intraday.json && jq .operationalData < nordstream-opal-intraday.json   > nordstream-opal-data-intraday.json	


wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=hour&periodize=0&pointDirection=pl-tso-0001itp-00104entry&timezone=UTC&to=${ENDDATE}" \
	-O yamal-kondratki-intraday.json && jq .operationalData < yamal-kondratki-intraday.json   > yamal-kondratki-data-intraday.json	


wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=hour&periodize=0&pointDirection=pl-tso-0002itp-00092entry&timezone=UTC&to=${ENDDATE}" \
	-O yamal-wysokoje-intraday.json && jq .operationalData < yamal-wysokoje-intraday.json   > yamal-wysokoje-data-intraday.json	
	
#wget "https://transparency.entsog.eu/api/v1/operationalData?from=${STARTDATE}&indicator=Physical%20Flow&limit=-1&periodType=hour&periodize=0&pointDirection=ua-tso-0001itp-10008exit&timezone=UTC&to=${ENDDATE}" \
#	-O hermanowice-intraday.json
#	
#jq .operationalData < hermanowice-intraday.json   > hermanowice-data-intraday.json
	


