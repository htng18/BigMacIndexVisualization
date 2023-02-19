'''
    This script is to be run in python shell in
    AWS Glue to transform the data from the source
    of BigMacIndex in S3. This calculates the BigMac
    exchange rate, actual exchange rate and their 
    evaluation in terms of USD. 

'''

import sys
from awsglue.utils import getResolvedOptions
import boto3
import pandas as pd

args = getResolvedOptions(sys.argv, ['s3_target_path_key', 's3_target_path_bucket'])
bucket = args['s3_target_path_bucket']
filename = args['s3_target_path_key']
outputfile = 'bigmacdata_processed.csv'

bigmac = pd.read_csv(f"s3://{bucket}/{filename}")

bigmac["dollar_price"] = bigmac["local_price"] / bigmac["dollar_ex"]
dollar_price = bigmac.pivot(index='date',columns='name',values='dollar_price').round(2)
GDP_dollar = bigmac.pivot(index='date',columns='name',values='GDP_dollar').round(2)
localprice = bigmac.pivot(index='date',columns='name',values='local_price')
USBMEX = localprice.div(localprice['United States'], axis=0)
USEX = bigmac.pivot(index='date',columns='name',values='dollar_ex')

column = list(USBMEX.columns)
countrylist = column
EXEVAL = pd.DataFrame()
for col in column:
    temp = round((USBMEX[col] - USEX[col])/USEX[col]*100,2)
    temp.columns = [col]
    EXEVAL = pd.concat([EXEVAL, temp], axis=1)
index = list(USBMEX.index)

namelist = bigmac['name'].tolist()
isoalpha3 = bigmac['iso_a3'].tolist()
countrymap = {i:"" for i in namelist}
for i,value in enumerate(namelist):
    countrymap[value] = isoalpha3[i]
newindex = []
for i in USBMEX.columns:
    newindex.append(countrymap[i])
print('OK2')

bigmac_data = pd.DataFrame()
for date in dollar_price.index:
    temp = pd.concat([dollar_price.loc[date], GDP_dollar.loc[date], USBMEX.loc[date], USEX.loc[date], 
                      EXEVAL.loc[date]], axis=1)
    temp.columns = ["dollar_price", "GDP_dollar", "BigMac Exchange Rate", "Actual Exchange Rate", "Evaluation"]
    temp["date"] = date
    newindex = []
    for i in temp.index:
        newindex.append(countrymap[i])
    temp["iso_alpha3"] = newindex
    bigmac_data = pd.concat([bigmac_data, temp])
    
bigmac_data.reset_index().rename(columns={"index":"country"}).to_csv(f"s3://{bucket}/{outputfile}")
