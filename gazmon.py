#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [9.5, 7]
import datetime
import pandas
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator, LogLocator, FixedLocator, FixedFormatter, NullLocator)


# In[2]:


prefix="/home/ahu/git/gazproject/"


# In[3]:


def cleanUp(v, fixTime=True):
    v["timestamp"]=pandas.to_datetime(v["periodTo"], utc=True)
    if(fixTime==True):
        v["timestamp"]=v["timestamp"].dt.strftime("%Y-%m-%d 06:00:00")
        v["timestamp"]=pandas.to_datetime(v["timestamp"])
    v.sort_values(["timestamp"], inplace=True)
    v.set_index("timestamp", inplace=True)
    print(v.index.min(), v.index.max())
    
uzhgorod = pandas.read_json(prefix+"uzhgorod-data.json")
nordstreamF = pandas.read_json(prefix+"nordstream-fluxsys-data.json")
nordstreamO = pandas.read_json(prefix+"nordstream-opal-data.json")
yamalK = pandas.read_json(prefix+"yamal-kondratki-data.json")
yamalW = pandas.read_json(prefix+"yamal-wysokoje-data.json")
hermanowice = pandas.read_json(prefix+"hermanowice-data.json")
strandzha2 = pandas.read_json(prefix+"strandzha2-data.json")


cleanUp(uzhgorod)
cleanUp(nordstreamF)
cleanUp(nordstreamO)
cleanUp(yamalK)
cleanUp(yamalW)
cleanUp(hermanowice)
cleanUp(strandzha2)

begindate=max([uzhgorod.index.min(), nordstreamF.index.min(), nordstreamO.index.min(), yamalW.index.min(), yamalK.index.min(), hermanowice.index.min(), strandzha2.index.min()])

enddate=min([uzhgorod.index.max(), nordstreamF.index.max(), nordstreamO.index.max(), yamalW.index.max(), yamalK.index.max(), hermanowice.index.max(), strandzha2.index.max()])
enddate


# In[4]:


yamalK_h = pandas.read_json(prefix+"yamal-kondratki-data-intraday.json")
yamalW_h = pandas.read_json(prefix+"yamal-wysokoje-data-intraday.json")
nordstreamF_h = pandas.read_json(prefix+"nordstream-fluxsys-data-intraday.json")
nordstreamO_h = pandas.read_json(prefix+"nordstream-opal-data-intraday.json")
uzhgorod_h = pandas.read_json(prefix+"uzhgorod-data-intraday.json")
strandzha2_h = pandas.read_json(prefix+"strandzha2-data-intraday.json")
cleanUp(yamalK_h, False)
cleanUp(yamalW_h, False)
cleanUp(nordstreamF_h, False)
cleanUp(nordstreamO_h, False)
cleanUp(uzhgorod_h, False)
cleanUp(strandzha2_h, False)


# In[5]:


storage = pandas.read_json(prefix+"storage.json")
storage["timestamp"]=pandas.to_datetime(storage["gasDayStartedOn"]) + datetime.timedelta(days=1)
storage.sort_values(["timestamp"], inplace=True)
storage.set_index("timestamp", inplace=True)
#storage=storage["2022-01-01":]
storage


# In[6]:


plt.figure()
# GWh/d - 
plt.plot(((storage.injection - storage.withdrawal)/24).rolling(1, center=True).mean())
plt.grid()
for y in range(2012, 2023): 
    plt.axvline(datetime.date(y, 3, 14), ls=':', color='red')

plt.ylabel("Gigawatts")


# In[7]:


plt.figure()
plt.plot(uzhgorod.value/24/1000000, label="Uzhgorod")
plt.plot(nordstreamF.value/24/1000000, label="Nordstream Greifswald Fluxsys")
plt.plot(nordstreamO.value/24/1000000, label="Nordstream Greifswald Opal")
plt.plot(yamalK.value/24/1000000, label="Yamal Kondratki")
plt.plot(yamalW.value/24/1000000, label="Yamal Wysokoje")
plt.plot(hermanowice.value/24/1000000, label="Hermanowice")
plt.plot(strandzha2.value/24/1000000, label="Turkstream Strandzha2")

#plt.xlim(begindate, enddate)
plt.plot((uzhgorod.value+yamalK.value+yamalW.value+nordstreamF.value+nordstreamO.value+hermanowice.value+strandzha2.value)/24000000, label="Sum")

plt.ylabel("GW")
plt.legend()
plt.title("Russian natural gas flow to Europe. Data from ENTSO-G\nGraph from https://berthub.eu/gazmon/")
plt.xticks(rotation=25)


plt.grid()


# In[8]:



fig, ax1 = plt.subplots()

ax1.plot((uzhgorod_h.value+yamalK_h.value+yamalW_h.value+nordstreamF_h.value+nordstreamO_h.value+strandzha2_h.value)/1000000, label="Sum")

ax1.plot(uzhgorod_h.value/1000000, label="Uzhgorod")
ax1.plot(nordstreamF_h.value/1000000, label="Nordstream Greifswald Fluxsys")
ax1.plot(nordstreamO_h.value/1000000, label="Nordstream Greifswald Opal")
ax1.plot(yamalK_h.value/1000000, label="Yamal Kondratki")
ax1.plot(yamalW_h.value/1000000, label="Yamal Wysokoje")
ax1.plot(strandzha2_h.value/1000000, label="Turkstream Strandzha2")

#plt.plot(hermanowice.value/24/1000000, label="Hermanowice")
#plt.xlim(begindate, enddate)


ax2 = ax1.twinx()
mn, mx = ax1.get_ylim() 
eurpermwh=100
ax2.set_ylim(1000 * mn * eurpermwh/1000000, 1000 * mx * eurpermwh/1000000)
ax2.set_ylabel('~M€/hour')
ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

ax1.set_ylabel("Gigawatt")
ax1.legend(loc=7)
plt.title("Russian natural gas flow to Europe (~100€/MWh). Hourly, last data point: "+nordstreamF_h.index.max().strftime("%Y-%m-%d %H:%M")+" UTC\nData from ENTSO-G, graph by https://berthub.eu/gazmon")
#ax1.xticks(rotation=25)
ax1.tick_params(labelrotation=45)


ax1.set_xlabel("UTC")
ax1.grid()
plt.tight_layout()
plt.savefig(prefix+"livegraph.png")


# In[9]:


def makeGraph(fname, limit=-1, reserves=False):
    global yamalK, yamalW, uzhgorod, nordstreamF, nordstreamO, hermanowice, uzghorod, strandzha2
    plt.figure()
    strandzha2=strandzha2[begindate:enddate]

    yamalK=yamalK[begindate:enddate]
    yamalW=yamalW[begindate:enddate]
    nordstreamO=nordstreamO[begindate:enddate]
    uzhgorod=uzhgorod[begindate:enddate]
    nordstreamF=nordstreamF[begindate:enddate]


    
    pal = [ "#44344f", "#98a6d4", "#5b9279", "#c2f970", "#112233", "#FFD700", "#0057B8", "red"]
    labels=[ "Hermanowice", "Yamal Wysokoje", "Yamal Kondratki", "Turkstream Strandzha2", "Nordstream OPAL", "Uzhgorod (Ukraine)", "Nordstream Fluxsys" ]
    locbegindate = begindate
    if limit >= 0:
        locbegindate = enddate - datetime.timedelta(days=7)
    
    plt.xlim(locbegindate, enddate)
    
    plt.stackplot(uzhgorod.index,
                hermanowice.value/24000000,
                yamalW.value/24000000,
                yamalK.value/24000000,
                strandzha2.value/24000000,
                nordstreamO.value/24000000,
                uzhgorod.value/24000000,              
                nordstreamF.value/24000000, 
                  
            colors=pal, labels=labels)

    
    plt.ylabel("Gigawatt")
    plt.xticks(rotation=25)
    if(limit < 0):
        labels = labels + list(["Start of invasion"])
        plt.axvline(datetime.date(2022, 2, 24), ls=':', color='red', label="Start of invasion")
        if(reserves==True):
            plt.ylim(-20, 360)
    else:
        plt.ylim(0, 200)

    if reserves==True:
        plt.title("Russian gas flow to Europe & EU storage withdrawals. Data from ENTSO-G & GIE,\n graph from https://berthub.eu/gazmon\nLast data point: "+enddate.strftime("%Y-%m-%d %H:%M"))

        plt.plot(-(storage.injection - storage.withdrawal)/24, label="EU storage withdrawal")
        labels = labels + list(["EU Storage withdrawal"])
        plt.legend(reversed(plt.legend().legendHandles), reversed(labels), loc=1)
    else:
        plt.title("Russian gas flow to Europe. Data from ENTSO-G, graph from https://berthub.eu/gazmon\nLast data point: "+enddate.strftime("%Y-%m-%d %H:%M"))
        plt.legend(reversed(plt.legend().legendHandles), reversed(labels), loc=2)
    

    plt.grid()
    plt.savefig(fname)
    
makeGraph(prefix+"/russian-gas.png")
makeGraph(prefix+"/russian-gas-week.png", 7)
makeGraph(prefix+"/russian-gas-reserves.png", reserves=True)
makeGraph(prefix+"/russian-gas-reserves-week.png", 7, reserves=True)

