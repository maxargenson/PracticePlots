#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 09:44:23 2024

@author: margenson
"""

from MaxOrderSummaryData import get_os_data
#from ExecQtyPlots import getExecQtyPlots
#from Utilities import SamplingFrequency,LogicalOperator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
                                                        #excluded clients
os_data_raw, os_data= get_os_data('data/os2023.csv',['QBDEVELOPER','QBPRODRISK'])

top_few_rows = os_data.head(40)



## Get the Top 10 Clients in order with size
client_totals = os_data.groupby('client')['size'].sum()
sorted_clients = client_totals.sort_values(ascending=True)
top_10_clients = sorted_clients.tail(10)

## Get the Algos with size, exclude STRIKER and SMARTDIRECT
algo_totals = os_data.groupby('targetstrat')['size'].sum()
algo_totals = algo_totals.drop(['SWITCHER', 'SMARTDIRECT'])

## Get the counts of each type of class
class_counts = os_data['class'].value_counts()

# Group the data by client AND targetstrat for the top 10 clients by size
filtered_os_data = os_data[os_data['client'].isin(top_10_clients.index)]
order_counts = filtered_os_data.groupby(['client', 'targetstrat']).size().unstack(fill_value=0)
order_counts = order_counts.loc[top_10_clients.index]
order_counts = order_counts.drop(['SWITCHER', 'SMARTDIRECT'], axis = 1)


'''
## Creating the Plots
fig, (ax1,ax2,ax3) = plt.subplots(3, 1, figsize=(15, 25))
formatter = FuncFormatter(lambda x, _: format(int(x), ','))  # Format integers with commas


### Cumulatize Size of Orders Per Clients
top_10_clients.plot(kind='bar', ax=ax1, color = 'slateblue' )
ax1.set_title("Cumulative Size of Orders Per Client")
ax1.set_xlabel("Clients")
ax1.set_ylabel("Cumulative Size of Orders")
ax1.set_xticklabels(top_10_clients.index, rotation = 45)
ax1.yaxis.set_major_formatter(formatter)

### Cumulatize Size of Orders Per ALGO 
algo_totals.plot(kind = 'bar', ax=ax2, color = 'firebrick')
ax2.set_title("Cumulative Size of Orders Per Algo")
ax2.set_xlabel("Algo")
ax2.set_ylabel("Cumulative Size of Orders")
ax2.set_xticklabels(algo_totals.index, rotation = 45)
ax2.yaxis.set_major_formatter(formatter)

### Circle Graph of the Different Financial Classes
ax3.pie(class_counts, labels = class_counts.index)
ax3.set_title('Distribution of Classes Traded')
ax3.legend(loc = 'upper left', bbox_to_anchor=(0.0, 1))

'''

fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(25, 15))
formatter = FuncFormatter(lambda x, _: format(int(x), ','))  # Format integers with commas

### Cumulatize Size of Orders Per Clients Layered with Algos used
order_counts.plot(kind='bar', ax=ax1, stacked = True, colormap = 'viridis' )
ax1.set_title("Cumulative Size of Orders and Algo Usage Per Client")
ax1.set_xlabel("Clients")
ax1.set_ylabel("Cumulative Size of Orders")
ax1.legend(title='Algo Used')
ax1.set_xticklabels(top_10_clients.index, rotation = 45)
ax1.yaxis.set_major_formatter(formatter)

### Circle Graph of the Different Financial Classes
ax2.pie(class_counts)
ax2.set_title('Distribution of Classes Traded')
ax2.legend(title = 'Classes Traded')

plt.tight_layout()
plt.show()
