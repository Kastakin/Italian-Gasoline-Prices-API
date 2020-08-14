from datetime import date

import pandas as pd
from dateutil.relativedelta import relativedelta


def load_place(csv):
    '''Load places data from CSV'''
    df = pd.read_csv(csv, skiprows=[0,1],index_col=0, header=None, sep=';', names=['id','owner','brand','type','name','address','town','state','lat','long'])
    return df

def load_price(csv):
    '''Load prices data from CSV'''
    df = pd.read_csv(csv, skiprows=[0,1], header=None, sep=';', names=['id','gastype','price','self','date'], dtype={'self': bool})

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M:%S').dt.date
    df = df.round({'price': 3})

    date_limit = date.today() - relativedelta(months=+1)
    df = df[df['date'] >= date_limit]
   
    return df
