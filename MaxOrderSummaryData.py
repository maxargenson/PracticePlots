import pandas as pd, time as tm, numpy as np, datetime

# Expected columns: class, ctype, slippages

def get_os_data(os_csv, excludedClients, startDate='', endDate=''):
    
    algoparams_mapping={
    'PercentVolume':            {'tag':8565,'type':float, 'displayValue':{'':np.nan}},
    'MustComplete':             {'tag':8610,'type':str, 'displayValue':{'':'MustComplete=No','0':'MustComplete=No','1':'MustComplete=Yes','':'MustComplete=No'}},
    'LiquidityAggressThreshold':{'tag':8590,'type':float, 'displayValue':{'':'0'}},
    'Duration':                 {'tag':8561,'type':float, 'displayValue':{'':np.nan}},
    'Mode':                     {'tag':8562,'type':str, 'displayValue':{'':'Mode=Normal','-1':'Mode=Passive','0':'Mode=Normal','1':'Mode=Aggressive','2':'Mode=2'}},
    'EventPause':               {'tag':8572,'type':str, 'displayValue':{'':'Pause during event','0':'Complete before event','1':'Pause during event','2':'Trade through event'}},
    'LegRiskTolerance':         {'tag':8571,'type':float, 'displayValue':{'':'0'}},
    'Legs':                     {'tag':8571,'type':float, 'displayValue':{'':'0'}},
    'NoCleanup':                {'tag':8589,'type':str, 'displayValue':{'':'clean up','0':'clean up','1':'No clean up'}},
    'Urgency':                  {'tag':8585,'type':str, 'displayValue':{'':'High','1':'High','2':'Ultra High'}},   
    'StrikerUrgency':           {'tag':8562,'type':str, 'displayValue':{'':'Normal','-1':'Passive','0':'Normal','1':'Aggressive'}},   
    'StrikerMode':              {'tag':8621,'type':str, 'displayValue':{'':'','0':'Arrival Price','1':'Target Price','2':'Delta Hedged Target Price'}}
    }
    
    #Upload data from csv
    tStart= tm.time()
    dfRaw= pd.read_csv(os_csv)
    print('{} imported in {:.1f} seconds'.format(os_csv, tm.time() - tStart))
    
    tStart= tm.time()
    df= dfRaw.copy(deep=True)
    #Apply a date filter when start and/or end dates are provided
    if startDate:
        df=df.loc[pd.to_datetime(df['date'])>=pd.to_datetime(startDate)]
    if endDate:
        df=df.loc[pd.to_datetime(df['date'])<=pd.to_datetime(endDate)]    
    #Exclude non-real clients
    df=df.loc[~df['client'].isin(excludedClients)]
    #Exclude LEGGER's leg orders
    df=df.loc[df['targetstrat']!='LEGGER']
    #Data formatting
    df['nchild']=df['nchild'].fillna(0).astype(int)
    df['algoparams']=df['algoparams'].fillna('').astype(str)
    df['algoversion']=df['algoversion'].fillna('N/A').astype(str)
    df['prate'].replace({'0w':0},inplace=True)                              #Ask Why?????
    df['prate']=df['prate'].fillna(0).astype(float)
    df['lmtconsdurpct']=df['lmtconsdurpct'].fillna(0).astype(float)
    df['povconsdurpct']=df['povconsdurpct'].fillna(0).astype(float)
    #df['PercentVolume']=df['PercentVolume'].fillna(1).astype(float)
    df['ref_volume']=df['ref_volume'].fillna(0).astype(float)
    df['ref_volume']=df['ref_volume'].apply(lambda x:max(0,x))
    df['ref_volatility']=df['ref_volatility'].fillna(0).astype(float)
    df['ref_volatility']=df['ref_volatility'].apply(lambda x:max(0,x))
    df['date']= df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())
    for col in ['tend','tstart']: df[col]=pd.to_datetime(df[col])
    for col in ['benchmark','targetstrat','ctype','exchange']: df[col]=df[col].fillna('N/A').astype(str)
    df['algoparams'] = df['algoparams'].apply(lambda x: dict((pair.split("=") if '=' in pair else [pair,'']) for pair in x.split(";")))
    # Data enrichment
    df['Month']=df['date'].apply(lambda x:'%s-%s.'%(x.year,'{:02}'.format(x.month)))
    df['Quarter']=df['date'].apply(lambda x:'%s-Q%s'%(x.year,pd.to_datetime(x).quarter))
    df['Year']=df['date'].apply(lambda x:'%s'%(x.year))
    # Parse the algoparams column and add column corresponding to specificied list of algo parameters
    for name in algoparams_mapping:
        tag= str(algoparams_mapping[name]['tag'])
        df[name]=df['algoparams'].apply(lambda x:x[tag] if tag in x else '')
        df[name]=df[name].replace(algoparams_mapping[name]['displayValue'])
        df[name]=df[name].astype(algoparams_mapping[name]['type'])
    # Data sorting
    df=df.sort_values(by=['date','client','parentid'],ascending=True)
    print('Data cleaned, formated and enriched in {:.1f} seconds'.format(tm.time() - tStart))
    
    return dfRaw, df