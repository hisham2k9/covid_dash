import pandas as pd
from models import death, recovery, newcase, deathdetail
import datetime

df_death=pd.read_excel(r'C:\BMH\Assistant Manager\ED_Lama\updated_covid.xlsx', sheet_name='death')
entries = []
for e in df_death.T.to_dict().values():
    entries.append(death(**e))

for item in entries:
    item.datetime_update=datetime.datetime.now()
death.objects.bulk_create(entries)

df_newcase=pd.read_excel(r'C:\BMH\Assistant Manager\ED_Lama\updated_covid.xlsx', sheet_name='newcase')
entries = []
for e in df_newcase.T.to_dict().values():
    entries.append(newcase(**e))

for item in entries:
    item.datetime_update=datetime.datetime.now()
newcase.objects.bulk_create(entries)

df_recovery=pd.read_excel(r'C:\BMH\Assistant Manager\ED_Lama\updated_covid.xlsx', sheet_name='recovery')
entries = []
for e in df_recovery.T.to_dict().values():
    entries.append(recovery(**e))

for item in entries:
    item.datetime_update=datetime.datetime.now()
recovery.objects.bulk_create(entries)



df_detail=pd.read_excel(r'C:\BMH\Assistant Manager\ED_Lama\updated_covid.xlsx', sheet_name='deathdetail')
print(df_detail)
entries = []
for e in df_detail.T.to_dict().values():
    entries.append(deathdetail(**e))

deathdetail.objects.bulk_create(entries)


df_pivot=pd.read_excel(r'C:\BMH\Assistant Manager\ED_Lama\updated_covid.xlsx', sheet_name='keycountries')
print(df_pivot)
entries = []
for e in df_pivot.T.to_dict().values():
    entries.append(keycountry(**e))
for item in entries:
    item.datetime_update=datetime.datetime.now()

keycountry.objects.bulk_create(entries)  


df_abroad=pd.read_excel(r'C:\BMH\Assistant Manager\ED_Lama\updated_covid.xlsx', sheet_name='indianabroad')
print(df_abroad)
entries = []
for e in df_abroad.T.to_dict().values():
    entries.append(indianabroad(**e))
for item in entries:
    item.datetime_update=datetime.datetime.now()

indianabroad.objects.bulk_create(entries)  
