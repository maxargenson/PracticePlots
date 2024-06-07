from MaxOrderSummaryData import get_os_data

#from ExecQtyPlots import getExecQtyPlots
#from Utilities import SamplingFrequency,LogicalOperator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from matplotlib.ticker import FuncFormatter

                                                        #excluded clients
os_data_raw, os_data= get_os_data('data/os2023.csv',['QBDEVELOPER','QBPRODRISK'])

date_range = list(os_data['date'])

os_data['date'] = pd.to_datetime(os_data['date'])

top = os_data.head(50).T

def formatting_xaxis(ax,date_range):
    ax.set_xlim(date_range[0], date_range[-1])
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=15))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b%y'))
    ax.tick_params(axis='x', rotation=0,bottom=False, top=False) 


def slippage_over_time(df, instrument):  
    # Filter the dataframe to only use data for the given instrument/class
    filtered_df = df.loc[df['class']==instrument].copy()
    #filter the dataframe to only look of slippage between a certain range
    filtered_df = filtered_df[(filtered_df['apslip'] < 3) & (filtered_df['apslip'] > -3)]
    
    filtered_df.loc[:,'month'] = filtered_df['date'].dt.to_period('M').astype(str)
    
    #create plot
    fig, (ax1) = plt.subplots(1, 1, figsize=(15,15))
    sns.boxplot(x='month', y='apslip', data=filtered_df, ax=ax1, notch=True)
    
    title = "Median AP Slippage for Class:" + instrument
    ax1.set_title(title)
    ax1.set_ylabel("Slippage - Arrival Price")
    ax1.set_xlabel("Month")
    ax1.xaxis.set_tick_params(rotation=45)
    #formatting_xaxis(ax1,date_range)
    plt.tight_layout()
    plt.show()
    
    
def strobe_duration_stats(df, client=None):
    
    #filter the dataframe to only include STROBE orders
    filtered_df = df[df['targetstrat']=='STROBE']
    #If a client is given, filter df to only have rows with those clients
    if client is not None:
        filtered_df = filtered_df[filtered_df['client']==client]
        if filtered_df.empty:
            print(f"No rows left after filtering by client: {client}.")
            return filtered_df
    
    #convert columns to datetime format
    filtered_df['date'] = pd.to_datetime(filtered_df['date'], errors='coerce')
    filtered_df['cxltime'] = pd.to_datetime(filtered_df['cxltime'], errors='coerce')
    filtered_df['tstart'] = pd.to_datetime(filtered_df['tstart'], errors='coerce')
        
    # Calculate the duration for cancelled orders
    cancelled_orders = filtered_df[filtered_df['duration'].isna()]
    non_cancelled_orders = filtered_df[~filtered_df['duration'].isna()]
    
    if not cancelled_orders.empty:
       cancelled_orders['duration'] = (cancelled_orders['cxltime'] - cancelled_orders['tstart']).dt.total_seconds() / 3600
    
    # Combine the two dataframes back together
    combined_df = pd.concat([cancelled_orders, non_cancelled_orders])
    
    combined_df['duration'] = pd.to_numeric(combined_df['duration'], errors='coerce')
    
    ### Plotting ###
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15,15))
    
    # ax1: scatter plot of duration of orders
    # scatterplot for non-cancelled orders
    ax1.scatter(pd.to_numeric(non_cancelled_orders['duration'], errors='coerce'), non_cancelled_orders['date'], color = "green", label = "Non-cancelled Orders",  alpha = 0.6)
    
    # scatterplot of cancelled orders
    ax1.scatter(pd.to_numeric(cancelled_orders['duration'], errors='coerce'), cancelled_orders['date'], color = "red", label = "Cancelled Orders",  alpha = 0.6)

    ax1.set_title("Distribution of Strobe Order Duration")
    ax1.set_xlabel("Order Duration (hours)")
    ax1.set_ylabel("Date")
    ax1.legend()
    ax1.grid(True)
    
    # ax2: boxplots of duration for the different classes
    boxplot_data = combined_df.dropna(subset=['duration'])
    boxplot_data = boxplot_data[(boxplot_data['duration'] < 10) & (boxplot_data['duration'] > -10)]
    

    sns.boxplot(x = 'duration', y = 'class', data=boxplot_data, ax=ax2, orient='h', notch=False)    
    ax2.set_xlabel("Order Duration (hours)")
    ax2.set_ylabel("Class")
    ax2.legend()
    
    
    plt.tight_layout()
    plt.show()
    
    return combined_df

slippage_over_time(os_data, "IR")


#filtered_df_strobe = strobe_duration_stats(os_data)





#filtered_df_strobe = filtered_df_strobe.head(100)
    