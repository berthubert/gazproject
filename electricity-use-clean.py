#!/usr/bin/env python3
# coding: utf-8

# In[74]:

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

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


# In[75]:


prefix="/home/ahu/git/gazproject/harvested/"
imgprefix="/home/ahu/git/gazproject/"


# In[87]:


nleng=pandas.read_csv(prefix+"nlprod-year.csv")
for d in range(2,31):
    fname=prefix+"nlprod-202204"+str(d).zfill(2)+".csv"
    try: 
        nlday=pandas.read_csv(fname)
    except:
        break
    nleng=pandas.concat([nleng,nlday])

nleng = nleng.drop_duplicates()
nleng[["begin", "end"]] = nleng['MTU'].str.split(' - ', 1, expand=True)
nleng["timestamp"]=pandas.to_datetime(nleng["begin"], format="%d.%m.%Y %H:%M", utc=True)
nleng.sort_values(["timestamp"], inplace=True)
nleng.set_index("timestamp", inplace=True)
nleng=nleng[nleng["Fossil Gas  - Actual Aggregated [MW]"] != "-"]
nleng["gaspower"]=pandas.to_numeric(nleng["Fossil Gas  - Actual Aggregated [MW]"])
nleng["coalpower"]=pandas.to_numeric(nleng["Fossil Hard coal  - Actual Aggregated [MW]"])
nleng["solarpower"]=pandas.to_numeric(nleng["Solar  - Actual Aggregated [MW]"])
nleng["windpower"]=pandas.to_numeric(nleng["Wind Offshore  - Actual Aggregated [MW]"]) + pandas.to_numeric(nleng["Wind Onshore  - Actual Aggregated [MW]"])
nleng["nukepower"]=pandas.to_numeric(nleng["Nuclear  - Actual Aggregated [MW]"])
nleng["wastepower"]=pandas.to_numeric(nleng["Waste  - Actual Aggregated [MW]"])
nleng["otherpower"]=pandas.to_numeric(nleng["Other  - Actual Aggregated [MW]"])
nleng.tail(4)


# In[88]:


def addATransport(df, name):
    nlyear = pandas.read_csv(prefix+name+"-year.csv")
    nlyear=nlyear[nlyear[nlyear.columns[1]] != "-"] # filter out empty lines
    nlyear=nlyear[nlyear[nlyear.columns[2]] != "-"] # filter out empty lines
    
    for d in range(2, 32):
        try:
            newday=pandas.read_csv(prefix+name+"-202204"+str(d).zfill(2)+".csv")
            newday=newday[newday[newday.columns[1]] != "-"] # filter out empty lines
            newday=newday[newday[newday.columns[2]] != "-"] # filter out empty lines
    
            nlyear=pandas.concat([nlyear, newday])
        except:
            break
    nltransp=nlyear.drop_duplicates(subset=['Time (UTC)'])
                                                    
    print(nltransp.columns[1])
    nltransp[["begin", "end"]] = nltransp['Time (UTC)'].str.split(' - ', 1, expand=True)
    nltransp["timestamp"]=pandas.to_datetime(nltransp["begin"], format="%d.%m.%Y %H:%M", utc=True)
    nltransp.sort_values(["timestamp"], inplace=True)
    nltransp.set_index("timestamp", inplace=True)
    
    nltransp[nltransp.columns[1]]=pandas.to_numeric(nltransp[nltransp.columns[1]])
    nltransp[nltransp.columns[2]]=pandas.to_numeric(nltransp[nltransp.columns[2]])
    nltransp=nltransp.drop("begin", axis=1)
    nltransp=nltransp.drop("end", axis=1)
    nltransp=nltransp.drop("Time (UTC)", axis=1)
    
    #plt.figure()
    #plt.title(name)
    #plt.plot(nltransp[nltransp.columns[0]] - nltransp[nltransp.columns[1]])
    nltransp=nltransp.resample("15T").interpolate("time")
    #plt.plot(nltransp[nltransp.columns[0]] - nltransp[nltransp.columns[1]], '-+')

    if(len(df)==0):
        print("Copying!")
        df=nltransp
    else:
        df=df.join(nltransp)
    print(len(df))
    return df

transp=pandas.DataFrame()
date="year"
transp=addATransport(transp, "nlbe")
transp=addATransport(transp, "nldk1")
transp=addATransport(transp, "nlde-lu")
transp=addATransport(transp, "nlgb")
transp=addATransport(transp, "nlno2")
importpower=(transp["BZN|BE > BZN|NL [MW]"] + transp["BZN|DE-LU > BZN|NL [MW]"] + transp["BZN|DK1 > BZN|NL [MW]"] + transp["BZN|GB > BZN|NL [MW]"] + transp["BZN|NO2 > BZN|NL [MW]"]) -          (transp["BZN|NL > BZN|BE [MW]"] + transp["BZN|NL > BZN|DE-LU [MW]"] + transp["BZN|NL > BZN|DK1 [MW]"] + transp["BZN|NL > BZN|GB [MW]"] + transp["BZN|NL > BZN|NO2 [MW]"])
transp


# In[89]:


#print(stukje.tail(10))
plt.figure()

start=datetime.datetime.now()-datetime.timedelta(days=2)

stukje=transp[start:]

plt.plot(stukje["BZN|BE > BZN|NL [MW]"] - stukje["BZN|NL > BZN|BE [MW]"], label="BE", alpha=0.4)
plt.plot(stukje["BZN|DE-LU > BZN|NL [MW]"] - stukje["BZN|NL > BZN|DE-LU [MW]"], label="DE-LU", alpha=0.4)
plt.plot(stukje["BZN|DK1 > BZN|NL [MW]"] - stukje["BZN|NL > BZN|DK1 [MW]"], label="DK1", alpha=0.4)
plt.plot(stukje["BZN|GB > BZN|NL [MW]"] - stukje["BZN|NL > BZN|GB [MW]"], label="GB", alpha=0.4)
plt.plot(stukje["BZN|NO2 > BZN|NL [MW]"] - stukje["BZN|NL > BZN|NO2 [MW]"], label="NO2", alpha=0.4)



plt.plot(importpower[start:],
        label="Total", lw=2)
plt.grid()
plt.legend()
plt.ylabel("MW")
plt.axhline(y=0, color='black', linestyle='-')
plt.title('Dutch electricity imports (positive values) and exports (negative values)')
plt.xlabel("UTC")
plt.savefig(imgprefix+"nl-exports.svg")


# In[90]:


plt.figure()
labels=["Nuke", "Coal", "Gas", "Some of the wind", "Other", "Waste", "A bit of the solar"]
start=datetime.datetime.now()-datetime.timedelta(days=2)
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

plt.plot(importpower[start:], color='red', label="Electricity imports")
#plt.legend(loc=2)
labels = labels + list(["Electricity imports"])

plt.legend(reversed(plt.legend().legendHandles), reversed(labels), loc=2)
#plt.gca().legend(handles[::-1], labels[::-1])#, loc='upper left')

plt.grid()
#plt.ylim(-6000,15000)
plt.xlabel("UTC")
plt.ylabel("MW")
plt.title("Dutch known electricity generation by source")
plt.savefig(imgprefix+"known-generation.svg")


# In[96]:


plt.figure()
labels=["Imports", "Nuke", "Coal", "Gas", "Other", "Waste"]
start=datetime.datetime.now()-datetime.timedelta(days=2)
restr=nleng[start:]
plt.stackplot(restr[:importpower.index.max()].index,
              importpower[start:],
              restr[:importpower.index.max()]["nukepower"],
              restr[:importpower.index.max()]["coalpower"],restr[:importpower.index.max()]["gaspower"],

                restr[:importpower.index.max()]["otherpower"], restr[:importpower.index.max()]["wastepower"], 
              labels=labels,
              colors=['grey', 'orange', 'black', 'steelblue', 'purple', 'brown']
             )

#plt.plot((restr["nukepower"]+restr["windpower"]+restr["coalpower"]+restr["gaspower"]+restr["otherpower"]).rolling("1h", center=True).mean(), label="Daily averaged sum")
#plt.plot((restr["nukepower"]+restr["windpower"]+restr["coalpower"]+restr["gaspower"]+restr["otherpower"]+importpower).rolling("1h", center=True).mean(), label="Daily averaged sum imp")

plt.plot(importpower[start:], color='red', label="Electricity imports")
#plt.legend(loc=2)
labels = labels + list(["Electricity imports"])

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


# In[93]:


plt.figure()
labels=["Export", "Import", "Gas"]#, "Nuke", "Coal", "Wind", "Gas", "Other", "Waste"]
restr=nleng.join(importpower.to_frame())
start=datetime.datetime.now()-datetime.timedelta(days=2)

small=restr[start:]
respower =(small["nukepower"]+small["coalpower"]+small["gaspower"]+small["otherpower"]+small["wastepower"])+small[0]
plt.plot(small[0], color='r', label="Net imports")
plt.bar(small.index, np.maximum(small[0], 0), width=1/(24*4.0), label="Imports", color='grey')
w=1.18/(24*4.0)
plt.bar(small.index, small["nukepower"], bottom=small[0], width=w, label="Nuclear", color='orange')
plt.bar(small.index, small["coalpower"], bottom=small[0]+small["nukepower"], width=w, label="Coal", color='black')
plt.bar(small.index, small["gaspower"], bottom=small[0]+small["nukepower"]+small["coalpower"], width=w, color='steelblue', label="Gas")
plt.bar(small.index, small["otherpower"], bottom=small[0]+small["nukepower"]+small["gaspower"]+small["coalpower"], width=w, label="Other", color='purple')
plt.bar(small.index, small["wastepower"], bottom=small[0]+small["otherpower"]+small["nukepower"]+small["gaspower"]+small["coalpower"], width=w, label="Waste", color='brown')


handles, labels = plt.gca().get_legend_handles_labels()
plt.gca().legend(handles[::-1], labels[::-1])#, loc='upper left')
plt.gcf().text(0.95, 0.6, "NL\n↑", fontsize=16, horizontalalignment='center')
plt.gcf().text(0.95, 0.2, "↓\nBE DE\nNO UK\nDK", fontsize=16, horizontalalignment='center')


plt.grid()
plt.xlabel("UTC")
plt.ylabel("MW")
plt.title("Dutch non-renewable electricity generation by source")
plt.axhline(y=0, color='black', linestyle='-')


# In[ ]:





# In[10]:


#print(importpower.resample("15T").interpolate("time"))
knownpower=(nleng["nukepower"]+nleng["coalpower"]+nleng["gaspower"]+nleng["otherpower"]+nleng["wastepower"])+importpower
# +nleng["windpower"] ++
#knownpower=knownpower["2022-04-01":"2022-04-25"]
print(knownpower.head(10))
plt.figure()
#
kpdf=knownpower.to_frame()
kpdf["time"]=pandas.to_datetime(kpdf.index.time.astype(str))
hh_mm = DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(hh_mm)

for dnum in [25, 26, 27, 28]:
    daystr="2022-04-"+str(dnum).zfill(2)
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

