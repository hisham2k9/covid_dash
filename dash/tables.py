import django_tables2 as tables
from dash.models import deathdetail,indianabroad
from django_tables2.utils import A


class deathdetailtable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover dataTable ",
                 'id':'table' }
        model=deathdetail
        fields=['death_number', 'death_date', 'age', 'gender','nationality','state',
                'suspected_reason','comorbidities','source']
        

class indianabroadtable(tables.Table):
    total = tables.Column(accessor=A('total_count'))
    
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover dataTable ",
                 'id':'table' }
        model=indianabroad
        fields=['country', 'active_cases', 'deaths']
        sequence = ['country', 'active_cases', 'deaths', 'total']
        
class statewisedetailtable(tables.Table):
    date=tables.Column()
    new_case=tables.Column()
    deaths=tables.Column()
    recovery=tables.Column()
    
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover dataTable ",
                 'id':'table' }
 
 
class indiatable(tables.Table):
    State=tables.Column()
    T=tables.Column()
    A=tables.Column()
    R=tables.Column()
    D=tables.Column()
    
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover dataTable  ",
                 'id':'table',
                 'style': "'width:10%'" }
             
    
    