import time
import requests
import xlsxwriter
import pandas as pd
from lxml import etree
from datetime import datetime

config = {
    'BankOfChina': {
        'link' : 'https://www.bankofchina.com/sourcedb/whpj/enindex_1619.html',
    },
    'CMBChina' : {
        'link': 'http://english.cmbchina.com/Rate/ForexRates.aspx',
        'xpath' : '//*[@id="rightpart"]/div[3]/div[2]/div[1]/text()',
    }
}

def requestFxTable(bankLink):
    # make a request to the website and asking for the table
    # Bank of China have different format and i have to clean it using loc
    if bankLink == config['BankOfChina']['link'] :
        df = pd.read_html(bankLink)[4].loc[4:31,:6]
        return df
    elif bankLink == config['CMBChina']['link'] :
        df = pd.read_html(bankLink)[0]
        return df
    
def enrich_time_prefix(df , bankLink):
    page = requests.get(bankLink)
    tree = etree.HTML(page.text)
    time_prefix = tree.xpath(config['CMBChina']['xpath'])
    time_prefix = time_prefix[1][:10]
    df['Time'] = time_prefix +' '+ df['Time']

def requestFxRate(bankLink):
    df = requestFxTable(bankLink)
    #change columns and rows to make the table more neat
    df.columns = df.iloc[0]
    df = df[1:]
    #add a request time to keep track 
    df['RequestTime_UK'] = datetime.now()
    if bankLink == config['CMBChina']['link'] :
        #CMB have slightly different time format thus need to add a prefix before time
        enrich_time_prefix(df, bankLink)
        return df
    return df

def dataWriter(bank):
    df_All = pd.read_excel('/Users/Ivy_li/Fx_Rate_{}.xlsx'.format(bank))
    df = requestFxRate(config[bank]['link'])
    df_All = df_All.append(df)
    df_All.to_excel('/Users/Ivy_li/Fx_Rate_{}.xlsx'.format(bank))

#Once you have got the data, you could store it into excel
count = 0
while count < 21600 :
    count += 1
    #request every 15 mins , you could change the frequency 
    time.sleep(60.0*15)
    #open excel and write the data
    for bank in config.keys():
        dataWriter( bank )
