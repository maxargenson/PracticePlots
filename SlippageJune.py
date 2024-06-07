#from ExecQtyPlots import getExecQtyPlots
#from Utilities import SamplingFrequency,LogicalOperator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from MaxOrderSummaryData import get_os_data

                                                        #excluded clients
os_data_raw, os_data= get_os_data('data/os2023.csv',['QBDEVELOPER','QBPRODRISK'], '2023-06-01', '2023-06-30')

top_few_rows = os_data.iloc[:150]

## Filter dataframe to only have one month
'''
os_data['date'] = pd.to_datetime(os_data['date'])
year = 2023
month = 6
june_os_data = os_data[(os_data['date'].dt.year) & (os_data['date'].dt.month)]
'''

## ax1 - Filter dataframe to only have the rows where benchmark is arrival price
ap_slippage_df = os_data[os_data['benchmark']=='ap']
ap_slippage_df = ap_slippage_df[(ap_slippage_df['apslip'] < 5) & (ap_slippage_df['apslip'] > -5)]

## ax2 - Filter dataframe to sample 4 weeks in June
ap_slippage_df['date'] = pd.to_datetime(ap_slippage_df['date'])
week_1 = ap_slippage_df[(ap_slippage_df['date'] > '2023-06-04') & (ap_slippage_df['date'] <= '2023-06-09')].copy()
week_2 = ap_slippage_df[(ap_slippage_df['date'] > '2023-06-11') & (ap_slippage_df['date'] <= '2023-06-16')].copy()
week_3 = ap_slippage_df[(ap_slippage_df['date'] > '2023-06-18') & (ap_slippage_df['date'] <= '2023-06-23')].copy()
week_4 = ap_slippage_df[(ap_slippage_df['date'] > '2023-06-25') & (ap_slippage_df['date'] <= '2023-06-30')].copy()

week_1['week'] = 'Week 1'
week_2['week'] = 'Week 2'
week_3['week'] = 'Week 3'
week_4['week'] = 'Week 4'

combined_df = pd.concat([week_1, week_2, week_3, week_4])


# Create Plot 
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15,15))
formatter = FuncFormatter(lambda x, _: format(int(x), ','))

# Create plot of ax1
norm = plt.Normalize(ap_slippage_df['apslip'].min(), ap_slippage_df['apslip'].max())
colors = plt.cm.seismic(norm(ap_slippage_df['apslip']))

ax1.scatter(ap_slippage_df['date'], ap_slippage_df['apslip'], c=colors)
ax1.set_title('Distribution of Arrival Price Slippage in June')
ax1.set_xlabel('Days')
ax1.set_ylabel('Slippage - Arrival Price')
ax1.grid(True)
ax1.invert_yaxis()

# Create plot of ax2
sns.violinplot(x='week', y='apslip', data = combined_df, ax=ax2)

ax2.set_title("Distribution of Arrival Price Slippage in June")
ax2.set_xlabel('Week')
ax2.set_ylabel('Slippage - Arrival Price')
ax2.invert_yaxis()


plt.tight_layout()
plt.show()