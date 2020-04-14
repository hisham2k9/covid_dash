from pandas import Series
import datetime
import pandas as pd
import requests


def _get_world_json():
    url = 'https://pomber.github.io/covid19/timeseries.json'
    r = requests.get(url)

    try:
        r.raise_for_status()
        return r.json()
    except:
        return None

def _get_india_json():
    url = 'https://api.covid19india.org/data.json'
    r = requests.get(url)

    try:
        r.raise_for_status()
        return r.json()
    except:
        return None


def worlddf():
    countries=['China', 'US', 'United Kingdom', 'Italy', 'France', 'Germany', 'Spain', 'Iran', 'India']
    json1=_get_world_json()
    dates=[]
    china=[]
    us=[]
    uk=[]
    italy=[]
    france=[]
    germany=[]
    spain=[]
    iran=[]
    india=[]
    i=0
    df=pd.DataFrame()
    for country in countries:
        if i==0:
            for items in json1[country]:
                newdate=datetime.datetime.strptime(items['date'], '%Y-%m-%d')
                #newdate=items['date']
                dates.append(newdate)
        #print(country)
        #selectcountry=(json1[country])
        for items in json1['China']:
            china.append(items['confirmed'])
        for items in json1['US']:
            us.append(items['confirmed'])
        for items in json1['United Kingdom']:
            uk.append(items['confirmed'])
        for items in json1['Italy']:
            italy.append(items['confirmed'])
        for items in json1['France']:
            france.append(items['confirmed'])
        for items in json1['Germany']:
            germany.append(items['confirmed'])
        for items in json1['Spain']:
            spain.append(items['confirmed'])
        for items in json1['Iran']:
            iran.append(items['confirmed'])
        for items in json1['India']:
            india.append(items['confirmed'])
        print(dates[1])
        if len(dates)==len(india):
            df['date']=pd.Series(dates,index=range(len(dates)))
            df['china']=pd.Series(china,index=range(len(dates)))
            df['us']=pd.Series(us,index=range(len(dates)))
            df['uk']=pd.Series(uk,index=range(len(dates)))
            df['italy']=pd.Series(italy,index=range(len(dates)))
            df['france']=pd.Series(france,index=range(len(dates)))
            df['germany']=pd.Series(germany,index=range(len(dates)))
            df['spain']=pd.Series(spain,index=range(len(dates)))
            df['iran']=pd.Series(iran,index=range(len(dates)))
            df['india']=pd.Series(india,index=range(len(dates)))

    total=[0 for i in range(len(df.columns.values))]
    total=pd.Series(total, index=df.columns.values)
    df=df.append(total, ignore_index=True)
    return df
    
def testcount(json):
    #print('reached json')
    testdic={}
    testdf=pd.DataFrame(columns=['date', 'tested'])
    today=datetime.date.today()-datetime.timedelta(days=1)
    #print(json['tested'][-1]['updatetimestamp'])
    for i in range(len(json['tested'])):
        print(json['tested'][i]['updatetimestamp'])
        date=datetime.datetime.strptime(json['tested'][i]['updatetimestamp'],'%d/%m/%Y %H:%M:%S').date()
        try:
            tested=int(json['tested'][i]['totalsamplestested'])
        except:
             tested=0
        testdic[date]=tested
    datevalues=list(testdic.keys())
    testvalues=list(testdic.values())
    
    datevalues.append('total')
    testvalues.append( 0)
    testdf['date']=datevalues
    testdf['tested']=testvalues
    
    return testdf
    
def seriesmaker(df,lis, dic,ser):
    ls=[]
    collist=df.columns.values
    for k,v in dic.items():
        if k !='total':
            ls.append(dic[k][0])
    lis=[datetime.datetime.now(), datetime.datetime.strptime(dic['total'][1], '%d/%m/%Y %H:%M:%S').date()]
    lis.extend(ls)
    #print('lis', lis)
    ser=pd.Series(lis, index=collist)
    return lis, dic, ser

def totmaker(df, fromlist):
    columns=df.columns.values
    i=0
    ls=[]
    #print(type(df))
    print(fromlist[1])
    if df['date'].iloc[-1].date()==fromlist[1]:
        df=df.drop(df.index[-1])
    for column in columns:
        if column !='date' and column != 'datetime_update':
            ls.append(df[column].sum(axis=0, skipna=True))
    ls.insert(0,0)
    ls.insert(0,0)
    #print('ls',ls)
    return ls, df

def diffmaker(ls1,ls,df):
    newl=[]
    collist=df.columns.values
    for i in range(len(ls1)):
        if (type(ls[i])==str):
            new=int(ls[i])-ls1[i]
            newl.append(new)
    newl.insert(0,datetime.date.today())
    newl.insert(0,0)
    news=pd.Series(newl, index=collist)
    return news

def dfupdater(df, dic,ser):
    if df['date'].iloc[-1].date()==datetime.datetime.strptime(dic['total'][1],'%d/%m/%Y %H:%M:%S').date():
        #print('if work')
        df=df.drop(df.index[-1])
        df=df.append(ser, ignore_index=True)
    else:
        #print('else work')
        df=df.append(ser, ignore_index=True)
    
    #print('ser', ser)
    
    #print('ser',ser)
    #print('df',df.head(2))
    #print('df',df.head(2))
    total=[0 for i in range(len(df.columns.values))]
   # print(total)
    total=pd.Series(total, index=df.columns.values)
    df=df.append(total, ignore_index=True)
    return df

def dateactuator(df, date='date'):
    for row in range(len(df[date])):
        try:
            #print(df[date].iloc[row].date())
            df[date].iloc[row]=df[date].iloc[row].date()
        except:
            pass
    return df

def worlddf():
    countries=['China', 'US', 'United Kingdom', 'Italy', 'France', 'Germany', 'Spain', 'Iran', 'India']
    json1=_get_world_json()
    dates=[]
    china=[]
    us=[]
    uk=[]
    italy=[]
    france=[]
    germany=[]
    spain=[]
    iran=[]
    india=[]
    i=0
    df=pd.DataFrame()
    for country in countries:
        if i==0:
            for items in json1[country]:
                dates.append(items['date'])
        #print(country)
        #selectcountry=(json1[country])
        for items in json1['China']:
            china.append(items['confirmed'])
        for items in json1['US']:
            us.append(items['confirmed'])
        for items in json1['United Kingdom']:
            uk.append(items['confirmed'])
        for items in json1['Italy']:
            italy.append(items['confirmed'])
        for items in json1['France']:
            france.append(items['confirmed'])
        for items in json1['Germany']:
            germany.append(items['confirmed'])
        for items in json1['Spain']:
            spain.append(items['confirmed'])
        for items in json1['Iran']:
            iran.append(items['confirmed'])
        for items in json1['India']:
            india.append(items['confirmed'])

        if len(dates)==len(india):
            df['date']=pd.Series(dates,index=range(len(dates)))
            df['china']=pd.Series(china,index=range(len(dates)))
            df['us']=pd.Series(us,index=range(len(dates)))
            df['uk']=pd.Series(uk,index=range(len(dates)))
            df['italy']=pd.Series(italy,index=range(len(dates)))
            df['france']=pd.Series(france,index=range(len(dates)))
            df['germany']=pd.Series(germany,index=range(len(dates)))
            df['spain']=pd.Series(spain,index=range(len(dates)))
            df['iran']=pd.Series(iran,index=range(len(dates)))
            df['india']=pd.Series(india,index=range(len(dates)))

    total=[0 for i in range(len(df.columns.values))]
    total=pd.Series(total, index=df.columns.values)
    df=df.append(total, ignore_index=True)
    
    return df


def mainman():
    json=_get_india_json()
    dic={'andaman_and_nicobar':'an','andhra_pradesh':'ap','arunachal_pradesh':'ar',
            'assam':'as','bihar':'br','chandigarh':'ch','chhattisgarh':'ct',
            'daman_n_diu':'dd','delhi':'dl','dadra_nagar_haveli':'dn','goa':'ga','gujarat':'gj',
            'himachal_pradesh':'hp','haryana':'hr',
            'jharkhand':'jh','jammu_and_kashmir':'jk','karnataka':'ka',
            'kerala':'kl','lakshadeep':'ld','ladakh':'la','maharashtra':'mh','meghalaya':'ml',
             'manipur':'mn',
            'madhya_pradesh':'mp',
            'mizoram':'mz',
            'nagaland':'nl','odisha':'or',
           'punjab':'pb', 
           'puducherry':'py',
            'rajasthan':'rj','sikkim':'sk','tamil_nadu':'tn','telangana':'tg','tripura':'tr',
            'uttar_pradesh':'up','uttarakhand':'ut',
            'west_bengal':'wb', 'total':'tt'
           }

    deathdict={}
    confirmeddict={}
    recovereddict={}
    deathlist=[]
    confirmedlist=[]
    recoveredlist=[]
    deathseries=pd.Series()
    confirmedseries=pd.Series()
    recoveredseries=pd.Series()

    ls=[] #temp list everywhere used
    df_death=pd.read_excel(r'updated_covid.xlsx', sheet_name='death',skipfooter=1)
    df_confirmed=pd.read_excel(r'updated_covid.xlsx', sheet_name='newcase',skipfooter=1)
    df_recovered=pd.read_excel(r'updated_covid.xlsx', sheet_name='recovery',skipfooter=1)
    df_testsdone=pd.read_excel(r'updated_covid.xlsx', sheet_name='testsdone',skipfooter=1)
    df_keycountries=pd.read_excel(r'updated_covid.xlsx', sheet_name='keycountries')
    df_deathdetail=pd.read_excel(r'updated_covid.xlsx', sheet_name='deathdetail')
    df_indianabroad=pd.read_excel(r'updated_covid.xlsx', sheet_name='indianabroad')
    
    for k,v in dic.items():
        for i in range(len(json['statewise'])):
            if dic[k]==json['statewise'][i]['statecode'].lower():
                deathdict[k]=[json['statewise'][i]['deaths'],json['statewise'][0]['lastupdatedtime']]
                confirmeddict[k]=[json['statewise'][i]['confirmed'],json['statewise'][0]['lastupdatedtime']]
                recovereddict[k]=[json['statewise'][i]['recovered'],json['statewise'][0]['lastupdatedtime']]
                
    deathlist, deathdict,deathseries=seriesmaker(df_death,deathlist, deathdict, deathseries)
    confirmedlist,confirmeddict, confirmedseries=seriesmaker(df_confirmed, confirmedlist, confirmeddict, confirmedseries)
    recoveredlist, recovereddict, recoveredseries=seriesmaker(df_recovered, recoveredlist, recovereddict, recoveredseries)


    deathlist1, df_death=totmaker(df_death, deathlist)
    confirmedlist1, df_confirmed=totmaker(df_confirmed, confirmedlist)
    recoveredlist1, df_recovered=totmaker(df_recovered, recoveredlist)


    newds=diffmaker(deathlist1,deathlist, df_death)
    newcs=diffmaker(confirmedlist1,confirmedlist,df_confirmed)
    newrs=diffmaker(recoveredlist1, recoveredlist,df_recovered)
    #print(newcs)
    #print(json)
    #print(df_death.head(2))
    df_death=dfupdater(df_death,deathdict,newds)
    df_confirmed=dfupdater(df_confirmed, confirmeddict, newcs)
    df_recovered=dfupdater(df_recovered,recovereddict,newrs)
    
    
    df_keycountries=worlddf()
    
    #correctin date from datetime obj
    
    df_death=dateactuator(df_death)
    df_confirmed=dateactuator(df_confirmed)
    df_recovered=dateactuator(df_recovered)
    df_keycountries=dateactuator(df_keycountries)
    df_deathdetail=dateactuator(df_deathdetail, date='death_date')
    
    #print(df_deathdetail['death_date'].head(2))
    #print(type(df_deathdetail['death_date'][1]))
    
    
    df_testsdone=testcount(json)
    
    
    
    
    
    
    #print(df_death.tail(4))
    #saving...
    writer = pd.ExcelWriter('updated_covid.xlsx', engine='xlsxwriter')
    df_death.to_excel(writer,sheet_name='death',index=None)
    df_confirmed.to_excel(writer, sheet_name='newcase', index=None)
    df_recovered.to_excel(writer, sheet_name='recovery', index=None)
    df_testsdone.to_excel(writer, sheet_name='testsdone', index=None)
    df_keycountries.to_excel(writer, sheet_name='keycountries', index=None)
    df_deathdetail.to_excel(writer, sheet_name='deathdetail', index=None)
    df_indianabroad.to_excel(writer, sheet_name='indianabroad', index=None)
    writer.save()
    