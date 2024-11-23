#!/usr/bin/env python3
# coding: utf-8

# In[1]:
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [11.5, 7]
import datetime
import pandas
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator, LogLocator, FixedLocator, FixedFormatter, NullLocator)



# In[2]:


prefix="/home/ahu/git/gazproject/"



storage = pandas.read_json(prefix+"storage-old.json")
storage = pandas.concat([storage,pandas.read_json(prefix+"storage-new.json")])
storage["timestamp"]=pandas.to_datetime(storage["gasDayStart"]) + datetime.timedelta(days=1)
storage.sort_values(["timestamp"], inplace=True)
storage.set_index("timestamp", inplace=True)
storage=storage["2021-01-01":]
storage["gasInStorage"]=storage['gasInStorage']
storage["injection"]=storage['injection']

storage["withdrawal"]=storage['withdrawal'] # .str.replace(',', '.').astype(float)

storage=storage[storage.gasInStorage < 10000]


# In[18]:


plt.figure()
plt.plot(1000*storage.gasInStorage/(365*24))   # TWh
plt.ylabel("GW*year")
plt.grid()
plt.ylim(0)
plt.axvline(datetime.datetime.today(), ls=':', color='red')
plt.axvline(datetime.datetime.today() - datetime.timedelta(days=365), ls=':', color='red')
plt.axvline(datetime.datetime.today() - datetime.timedelta(days=2*365), ls=':', color='red')
plt.axvline(datetime.datetime.today() - datetime.timedelta(days=3*365), ls=':', color='red')

for dates in [[datetime.datetime.today() - datetime.timedelta(days=3*365), datetime.datetime(2022,4,20)],
            [datetime.datetime.today() - datetime.timedelta(days=2*365), datetime.datetime(2023,4,20)],
              [datetime.datetime.today() - datetime.timedelta(days=365), datetime.datetime(2024,4,20)],
              [datetime.datetime.today() - datetime.timedelta(days=0),  datetime.datetime(2025,4,20)]]:
    weekpart=storage[dates[0] - datetime.timedelta(days=14):dates[0]]

    plt.plot([weekpart.index.min(), dates[1]], 
         [1000*weekpart.head(1).gasInStorage/(365*24), 
          1000*weekpart.head(1).gasInStorage/(365*24) + (dates[1]-weekpart.index.min()).days*1000*weekpart.gasInStorage.diff().mean()/(365*24)],
        ':', label="Trend "+weekpart.index.min().strftime("%Y-%m-%d")+" to "+weekpart.index.max().strftime("%Y-%m-%d"))

plt.legend()
plt.title("Energy content of gas storage sites in the EU\nData by Gas Infrastructure Europe (GIE.eu)")
plt.savefig(prefix+"gascontent.svg")


# In[ ]:


plt.figure()
# GWh/d - 
plt.plot(((storage.injection - storage.withdrawal)/24).rolling(7, center=True).mean())
plt.grid()
for y in range(2021, 2023): 
    plt.axvline(datetime.date(y, 6, 19), ls=':', color='red')

plt.ylabel("Gigawatts")

