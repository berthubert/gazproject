#!/usr/bin/env python3
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


# In[ ]:


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

# hermanowice.index.min(),
begindate=max([uzhgorod.index.min(), nordstreamF.index.min(), nordstreamO.index.min(), yamalW.index.min(), yamalK.index.min(),  strandzha2.index.min()])
# , hermanowice.index.max()
enddate=min([uzhgorod.index.max(), nordstreamF.index.max(), nordstreamO.index.max(), yamalW.index.max(), yamalK.index.max(), strandzha2.index.max()])
enddate


# In[ ]:


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


# In[6]:


storage = pandas.read_json(prefix+"storage-old.json")
storage = pandas.concat([storage,pandas.read_json(prefix+"storage-new.json")])
storage["timestamp"]=pandas.to_datetime(storage["gasDayStart"]) + datetime.timedelta(days=1)
storage.sort_values(["timestamp"], inplace=True)
storage.set_index("timestamp", inplace=True)
#storage=storage["2022-01-01":]
storage["gasInStorage"]=storage['gasInStorage']
storage["injection"]=storage['injection']

storage["withdrawal"]=storage['withdrawal'] # .str.replace(',', '.').astype(float)

storage=storage[storage.gasInStorage < 10000]


# In[9]:


plt.figure()
plt.plot(1000*storage.gasInStorage/(365*24))   # TWh
plt.ylabel("GW*year")
plt.grid()
plt.ylim(0)
plt.axvline(datetime.datetime.today(), ls=':', color='red')
plt.axvline(datetime.datetime.today() - datetime.timedelta(days=365), ls=':', color='red')

plt.axvline(datetime.datetime.today() - datetime.timedelta(days=2*365), ls=':', color='red')

for dates in [[datetime.datetime.today() - datetime.timedelta(days=3*365-10), datetime.datetime(2020,4,20)],
            [datetime.datetime.today() - datetime.timedelta(days=2*365), datetime.datetime(2021,4,20)],
              [datetime.datetime.today() - datetime.timedelta(days=365), datetime.datetime(2022,4,20)],
              [datetime.datetime.today() - datetime.timedelta(days=0),  datetime.datetime(2023,4,20)]]:
    weekpart=storage[dates[0] - datetime.timedelta(days=7):dates[0]]

    plt.plot([weekpart.index.min(), dates[1]], 
         [1000*weekpart.head(1).gasInStorage/(365*24), 
          1000*weekpart.head(1).gasInStorage/(365*24) + (dates[1]-weekpart.index.min()).days*1000*weekpart.gasInStorage.diff().mean()/(365*24)],
        ':', color='black')
    
plt.title("Energy content of gas storage sites in the EU")
plt.savefig(prefix+"gascontent.svg")


# In[ ]:


plt.figure()
# GWh/d - 
plt.plot(((storage.injection - storage.withdrawal)/24).rolling(7, center=True).mean())
plt.grid()
for y in range(2021, 2023): 
    plt.axvline(datetime.date(y, 6, 19), ls=':', color='red')

plt.ylabel("Gigawatts")


# In[ ]:


plt.figure()
plt.plot(uzhgorod.value/24/1000000, label="Uzhgorod")
plt.plot(nordstreamF.value/24/1000000, label="Nordstream Greifswald Fluxys")
plt.plot(nordstreamO.value/24/1000000, label="Nordstream Greifswald Opal")
#plt.plot(yamalK.value/24/1000000, label="Yamal Kondratki")
#plt.plot(yamalW.value/24/1000000, label="Yamal Wysokoje")
#plt.plot(hermanowice.value/24/1000000, label="Hermanowice")
#plt.plot(strandzha2.value/24/1000000, label="Turkstream Strandzha2")

#plt.xlim(begindate, enddate)
#plt.plot((uzhgorod.value+yamalK.value+yamalW.value+nordstreamF.value+nordstreamO.value+hermanowice.value+strandzha2.value)/24000000, label="Sum")

plt.ylabel("GW")
plt.legend()
plt.title("Russian natural gas flow to Europe. Data from ENTSO-G\nGraph from https://berthub.eu/gazmon/")
plt.xticks(rotation=25)


plt.grid()


# In[ ]:


fig, ax1 = plt.subplots()

ax1.plot((uzhgorod_h.value+yamalK_h.value+yamalW_h.value+nordstreamF_h.value+nordstreamO_h.value+strandzha2_h.value)/1000000, label="Sum")

ax1.plot(uzhgorod_h.value/1000000, label="Uzhgorod")
ax1.plot(nordstreamF_h.value/1000000, label="Nordstream Greifswald Fluxys")
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
ax1.legend(loc=2)
plt.title("Russian natural gas flow to Europe (~100€/MWh). Hourly, last data point: "+nordstreamF_h.index.max().strftime("%Y-%m-%d %H:%M")+" UTC\nData from ENTSO-G, graph by https://berthub.eu/gazmon")
#ax1.xticks(rotation=25)
ax1.tick_params(labelrotation=45)


ax1.set_xlabel("UTC")
ax1.grid()
plt.tight_layout()
plt.savefig(prefix+"livegraph.png")
plt.savefig(prefix+"livegraph.svg")


# In[ ]:


def makeGraph(fname, limit=-1, reserves=False):
    global yamalK, yamalW, uzhgorod, nordstreamF, nordstreamO, hermanowice, uzghorod, strandzha2
    plt.figure()

    locbegindate = begindate
    if limit >= 0:
        locbegindate = enddate - datetime.timedelta(days=7)
    
    yamalWL=yamalW[locbegindate:enddate]  
    yamalKL=yamalK[locbegindate:enddate]
    strandzha2L=strandzha2[locbegindate:enddate]
    nordstreamOL=nordstreamO[locbegindate:enddate]
    

    uzhgorodL=uzhgorod[locbegindate:enddate]
    nordstreamFL=nordstreamF[locbegindate:enddate]


    # "#44344f",
    pal = [  "#98a6d4", "#5b9279", "#c2f970", "#112233", "#FFD700", "#0057B8", "red"]
    labels=[  "Yamal Wysokoje", "Yamal Kondratki", "Turkstream Strandzha2", "Nordstream OPAL", "Uzhgorod (Ukraine)", "Nordstream Fluxys" ]
    # "Hermanowice",
    
    plt.stackplot(uzhgorodL.index,
               # hermanowice.value/24000000,
                yamalWL.value/24000000,
                yamalKL.value/24000000,
                strandzha2L.value/24000000,
                nordstreamOL.value/24000000,
                uzhgorodL.value/24000000,              
                nordstreamFL.value/24000000, 
                  
            colors=pal, labels=labels)

    
    plt.ylabel("Gigawatt")
    plt.xticks(rotation=25)
    if(limit < 0):
        labels = labels + list([ "Stop of Poland & Bulgaria", "Start of invasion"])
        plt.axvline(datetime.date(2022, 4, 28), ls=':', color='black', label="Stop of Poland & Bulgaria")      
        plt.axvline(datetime.date(2022, 2, 24), ls=':', color='red', label="Start of invasion")

        #if(reserves==True):
        #    plt.ylim(-200, 360)
    #else:
    #    labels = labels + list([ "Stop of Poland & Bulgaria"])
    #    plt.axvline(datetime.date(2022, 4, 28), ls=':', color='black', label="Stop of Poland & Bulgaria")      
    
    if reserves==True:
        plt.title("Russian gas flow to Europe & EU storage withdrawals. Data from ENTSO-G & GIE,\n graph from https://berthub.eu/gazmon\nLast data point: "+enddate.strftime("%Y-%m-%d %H:%M"))

        plt.plot((+(storage.injection - storage.withdrawal)/24)[locbegindate:enddate], label="EU storage withdrawal")
        labels = labels + list(["EU Storage injection"])
        plt.legend(reversed(plt.legend().legendHandles), reversed(labels))
    else:
        plt.title("Russian gas flow to Europe. Data from ENTSO-G, graph from https://berthub.eu/gazmon\nLast data point: "+enddate.strftime("%Y-%m-%d %H:%M"))
        plt.legend(reversed(plt.legend().legendHandles), reversed(labels))
    

    plt.grid()
    plt.savefig(fname+".png")
    plt.savefig(fname+".svg")
    
makeGraph(prefix+"/russian-gas")
makeGraph(prefix+"/russian-gas-week", 7)
makeGraph(prefix+"/russian-gas-reserves", reserves=True)
makeGraph(prefix+"/russian-gas-reserves-week", 7, reserves=True)


# In[ ]:





# In[ ]:




