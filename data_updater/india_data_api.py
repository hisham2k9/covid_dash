from pandas import Series
import datetime
import pandas as pd
import requests
from dash.models import death, recovery, newcase, deathdetail, testcount,keycountry,indianabroad, feedback
from apscheduler.schedulers.background import BackgroundScheduler
from data_updater.india_data_maker import mainman
#from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
#from django.conf import settings

def _get_india_json():
    url = 'https://api.covid19india.org/states_daily.json'
    r = requests.get(url)

    try:
        r.raise_for_status()
        return r.json()
    except:
        return None
    


def india_df_maker(df, today_data,string):
    ls=[]
    for data in today_data:
        if data['status']==string:
            data1=data.copy()
            del data1['status']
            del data1['tt']
            date_string= data1.pop('date')
            date_object=datetime.strptime(date_string, '%d-%b-%y')
            #del data1['date']
            ls=list(data1.values())
            ls.insert(0, date_object)
            ls.insert(0, None)
            _index=list(df.columns.values)
            series=pd.Series(ls, index=_index)
            df=df.append(series, ignore_index=True)
            df=df.append( series, ignore_index=True) #adds an extra row for total , coz skips last row when reading 
            df.iloc[-1,0]='total'
            df.iloc[-1,1]='nil'
    return df
            
def resetter():
    death.objects.all().delete()
    recovery.objects.all().delete()
    newcase.objects.all().delete()
    deathdetail.objects.all().delete()
    testcount.objects.all().delete()
    keycountry.objects.all().delete()
    indianabroad.objects.all().delete()
    
    
    
    df_death=pd.read_excel(r'updated_covid.xlsx', sheet_name='death',skipfooter=1)
    entries = []
    for e in df_death.T.to_dict().values():
        entries.append(death(**e))

    for item in entries:
        item.datetime_update=datetime.datetime.now()
    death.objects.bulk_create(entries)

    df_newcase=pd.read_excel(r'updated_covid.xlsx', sheet_name='newcase',skipfooter=1)
    entries = []
    for e in df_newcase.T.to_dict().values():
        entries.append(newcase(**e))

    for item in entries:
        item.datetime_update=datetime.datetime.now()
    newcase.objects.bulk_create(entries)

    df_recovery=pd.read_excel(r'updated_covid.xlsx', sheet_name='recovery',skipfooter=1)
    entries = []
    for e in df_recovery.T.to_dict().values():
        entries.append(recovery(**e))

    for item in entries:
        item.datetime_update=datetime.datetime.now()
    recovery.objects.bulk_create(entries)

    df_test=pd.read_excel(r'updated_covid.xlsx', sheet_name='testsdone', skipfooter=1)
    entries = []
    for e in df_test.T.to_dict().values():
        entries.append(testcount(**e))

    testcount.objects.bulk_create(entries)

    df_detail=pd.read_excel(r'updated_covid.xlsx', sheet_name='deathdetail',skipfooter=1)
    #print(df_detail)
    entries = []
    for e in df_detail.T.to_dict().values():
        entries.append(deathdetail(**e))

    deathdetail.objects.bulk_create(entries)


    df_pivot=pd.read_excel(r'updated_covid.xlsx', sheet_name='keycountries',skipfooter=1)
    #print(df_pivot)
    entries = []
    for e in df_pivot.T.to_dict().values():
        entries.append(keycountry(**e))
    for item in entries:
        item.datetime_update=datetime.datetime.now()

    keycountry.objects.bulk_create(entries)  


    df_abroad=pd.read_excel(r'updated_covid.xlsx', sheet_name='indianabroad',skipfooter=1)
    #print(df_abroad)
    entries = []
    for e in df_abroad.T.to_dict().values():
        entries.append(indianabroad(**e))
    for item in entries:
        item.datetime_update=datetime.datetime.now()
    indianabroad.objects.bulk_create(entries)


def update_india_data():
    print('update started')
    mainman()
    print('mainman job done')
    resetter()
    print('update completed')




    
    
    
#start()
