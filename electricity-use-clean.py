#!/usr/bin/env python3
# coding: utf-8

# In[16]:


from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import pytz

import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [9.5, 7]
import datetime
import pandas
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator, LogLocator, FixedLocator, FixedFormatter, NullLocator)
from matplotlib.dates import DateFormatter
from matplotlib.animation import FuncAnimation
from datetime import timedelta

import itertools

import matplotlib.animation as animation
import numpy as np
from entsoe import EntsoePandasClient



# In[17]:


# Does only realtime queries. If anything fails, exit


# In[18]:


imgprefix="/home/ahu/git/gazproject/"


# In[19]:


f=open("entso-e.key","r")
lines=f.readlines()
ekey=lines[0].strip()
f.close()


# In[26]:


eclient=EntsoePandasClient(api_key=ekey)

start=pandas.Timestamp.today(tz="Europe/Brussels")  -pandas.Timedelta('2 days')   
end=pandas.Timestamp.today(tz="Europe/Brussels") +pandas.Timedelta('1 days')     

nleng=eclient.query_generation("NL", start=start, end=end)
nleng["gaspower"]=nleng["Fossil Gas"]["Actual Aggregated"]
nleng["coalpower"]=nleng["Fossil Hard coal"]["Actual Aggregated"]
nleng["nukepower"]=nleng["Nuclear"]["Actual Aggregated"]
nleng["solarpower"]=nleng["Solar"]["Actual Aggregated"]
nleng["windpower"]=nleng["Wind Offshore"]["Actual Aggregated"] + nleng["Wind Onshore"]["Actual Aggregated"]
nleng["wastepower"]=nleng["Waste"]["Actual Aggregated"]
nleng["otherpower"]=nleng["Other"]["Actual Aggregated"] - nleng["Other"]["Actual Consumption"]
nleng=nleng.resample("15T").interpolate(method="time")


# In[27]:


#transp=eclient.query_import("NL", start, end)
#transp
# from, to
nltransp=pandas.DataFrame()
for c in ["DE_LU", "BE", "GB", "DK_1", "NO_2"]:
    exp=eclient.query_crossborder_flows("NL", c, start=start, end=end).to_frame("exp "+c)
    imp=eclient.query_crossborder_flows(c, "NL", start=start, end=end).to_frame("imp "+c)
    res=exp.join(imp)
    res["net "+c] = res["imp "+c] - res["exp "+c]
    if(len(nltransp)==0):
        nltransp = res
    else:
        nltransp = nltransp.join(res)

        

        
nltransp.interpolate(method="time", inplace=True)
nltransp["net"] = nltransp["net "+"DE_LU"]   
for c in ["BE", "GB", "DK_1", "NO_2"]:
    nltransp["net"] = nltransp["net"] + nltransp["net "+c]


# In[28]:


nltransp.net


# In[29]:


plt.figure()
for c in ["DE_LU", "BE", "GB", "DK_1", "NO_2"]:
    plt.plot(nltransp["net "+c], label=c, alpha=0.4)

plt.plot(nltransp["net"], label="Total")    

plt.legend()


# In[30]:


nlprices=eclient.query_day_ahead_prices("NL", start=start,end=end).to_frame("price")


# In[32]:


fig, ax1 = plt.subplots()
sel=nlprices[pandas.Timestamp.today(tz="Europe/Brussels")  -pandas.Timedelta('1 days'):]

ax1.plot(sel.index.tz_convert(tz="Europe/Amsterdam"), sel.price, label="Hourly")
#ax1.plot(sel.price.rolling("1d").mean(center=True), label="1 day average")
#ax1.plot(sel.price.rolling("7d").mean(center=True), label="7 day average")
ax1.axhline(0, color='black', linestyle='-')

ax2 = ax1.twinx()
mn, mx = ax1.get_ylim() 
ax2.set_ylim(0.1 * mn , 0.1 * mx)
ax2.set_ylabel('cent/kWh')
ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))


ax1.grid()
ax1.set_title("Dutch day-ahead electricity prices")
ax1.set_ylabel("EUR/MWh")
#ax1.set_ylim(0)
ax1.set_xlabel("Local time")
ax1.legend()
plt.savefig("day-ahead.svg")


# In[33]:


#print(stukje.tail(10))
plt.figure()

start=pytz.utc.localize(datetime.datetime.now()-datetime.timedelta(days=2))
print(start)
stukje=nltransp[start:]

for c in ["DE_LU", "BE", "GB", "DK_1", "NO_2"]:
    plt.plot(stukje["net "+c], label=c, alpha=0.4)


plt.plot(stukje.net,
        label="Total", lw=2)
plt.grid()
plt.legend()
plt.ylabel("MW")
plt.axhline(y=0, color='black', linestyle='-')
plt.title('Dutch electricity imports (positive values) and exports (negative values)')
plt.xlabel("UTC")
plt.savefig(imgprefix+"nl-exports.svg")


# In[34]:


plt.figure()
labels=["Nuke", "Coal", "Gas", "Some of the wind", "Other", "Waste", "A bit of the solar"]
start=pytz.utc.localize(datetime.datetime.now()-datetime.timedelta(days=2))

restr=nleng[start:]
plt.stackplot(restr.index,
              restr["nukepower"],
              restr["coalpower"],restr["gaspower"],

                restr["windpower"],
                restr["otherpower"], restr["wastepower"], restr["solarpower"],
              labels=labels,
              colors=['orange', 'black', 'steelblue', 'green', 'purple', 'brown', 'yellow']
             )

#plt.plot((restr["nukepower"]+restr["windpower"]+restr["coalpower"]+restr["gaspower"]+restr["otherpower"]).rolling("1h", center=True).mean(), label="Daily averaged sum")
#plt.plot((restr["nukepower"]+restr["windpower"]+restr["coalpower"]+restr["gaspower"]+restr["otherpower"]+importpower).rolling("1h", center=True).mean(), label="Daily averaged sum imp")

plt.plot(nltransp[start:].net, color='red', label="Electricity imports/exports")
#plt.legend(loc=2)
labels = labels + list(["Electricity imports/exports"])

plt.legend(reversed(plt.legend().legendHandles), reversed(labels), loc=2)
#plt.gca().legend(handles[::-1], labels[::-1])#, loc='upper left')

plt.grid()
#plt.ylim(-6000,15000)
plt.xlabel("UTC")
plt.ylabel("MW")
plt.title("Dutch known electricity generation by source")
plt.savefig(imgprefix+"known-generation.svg")


# In[35]:


plt.figure()
labels=["Imports/Exports", "Nuke", "Coal", "Gas", "Other", "Waste"]
start=pytz.utc.localize(datetime.datetime.now()-datetime.timedelta(days=2))

restr=nleng[start:nltransp.index.max()]
resnltransp=nltransp[restr.index.min():restr.index.max()]

print(len(restr[:resnltransp.index.max()]))
print(len(resnltransp[start:]))
print(len(restr[:resnltransp.index.max()]["nukepower"]))
print(len(restr[:resnltransp.index.max()]["coalpower"]))

plt.stackplot(restr[:resnltransp.index.max()].index,
              resnltransp[start:].net,
              restr[:resnltransp.index.max()]["nukepower"],
              restr[:resnltransp.index.max()]["coalpower"],restr[:resnltransp.index.max()]["gaspower"],

                restr[:resnltransp.index.max()]["otherpower"], restr[:resnltransp.index.max()]["wastepower"], 
              labels=labels,
              colors=['grey', 'orange', 'black', 'steelblue', 'purple', 'brown']
             )

#plt.plot((restr["nukepower"]+restr["windpower"]+restr["coalpower"]+restr["gaspower"]+restr["otherpower"]).rolling("1h", center=True).mean(), label="Daily averaged sum")
#plt.plot((restr["nukepower"]+restr["windpower"]+restr["coalpower"]+restr["gaspower"]+restr["otherpower"]+resnltransp).rolling("1h", center=True).mean(), label="Daily averaged sum imp")

plt.plot(resnltransp[start:].net, color='red', label="Electricity imports/exports")
#plt.legend(loc=2)
labels = labels + list(["Electricity imports/exports"])

plt.legend(reversed(plt.legend().legendHandles), reversed(labels), loc=2)
#plt.gca().legend(handles[::-1], labels[::-1])#, loc='upper left')
plt.axhline(y=0, color='black', linestyle='-')
plt.gcf().text(0.95, 0.6, "NL\n↑", fontsize=16, horizontalalignment='center')
plt.gcf().text(0.95, 0.2, "↓\nBE DE\nNO UK\nDK", fontsize=16, horizontalalignment='center')

plt.grid()
#plt.ylim(-6000,15000)
plt.xlabel("UTC")
plt.ylabel("MW")
plt.title("Dutch non-renewable electricity generation by source")

plt.savefig(imgprefix+"dutch-stack.svg")
plt.savefig(imgprefix+"dutch-stack.png")


# In[36]:


#print(importpower.resample("15T").interpolate("time"))
knownpower=(nleng["nukepower"]+nleng["coalpower"]+nleng["gaspower"]+nleng["otherpower"]+nleng["wastepower"])+nltransp.net
# +nleng["windpower"] ++
#knownpower=knownpower["2022-04-01":"2022-04-25"]
print(knownpower.tail(10))
plt.figure()
#
kpdf=knownpower.to_frame()
kpdf["time"]=pandas.to_datetime(kpdf.index.time.astype(str))
hh_mm = DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(hh_mm)

for dnum in [13,14]:
    daystr="2022-08-"+str(dnum).zfill(2)
    day=kpdf.loc[daystr]
    plt.plot(day.time, day[0], label=daystr, alpha=0.9)

  
weekavg=kpdf.groupby(["time"])[0].mean()
#weekavg.plot(label="Average")

plt.yticks(np.arange(-5000, 10000, 1000))

plt.ylim(-4000)
plt.grid()
plt.legend(loc=2)
plt.ylabel("MW")
plt.title("Dutch non-renewable electricity production & all imports for national use")
plt.xlabel("UTC")

plt.axhline(y=0, color='black', linestyle='-')
plt.savefig(imgprefix+"nlduck.svg")


# In[37]:


plt.figure()

restr=restr[start:]
plt.plot(restr["gaspower"], label="Gas", color='steelblue')
plt.plot(restr["coalpower"], label="Coal", color='black')
plt.plot(restr["windpower"], label="Some of the wind", color='green')
plt.plot(restr["solarpower"], label="Tiny bit of solar", color='yellow', lw=2)
#plt.plot(restr["solarpower"]*90, label="Estimate of solar", color='yellow', lw=2)

plt.plot(restr["nukepower"], label="Nuclear",color='orange')
plt.plot(restr["wastepower"], label="Waste", color='brown')
plt.plot(restr["otherpower"], label="Other", color='purple')

plt.grid()
plt.ylim(1)
plt.yscale("log")
plt.ylabel("MW")
plt.title("ENTSO-E / TenneT Dutch known/reported electricity production")
#plt.axhline(y=restr.nukepower.quantile(0.99), color='black', linestyle='-')
plt.xlabel("UTC")
plt.legend()
plt.savefig(imgprefix+"tennet-total.svg")


# In[ ]:





# In[ ]:




