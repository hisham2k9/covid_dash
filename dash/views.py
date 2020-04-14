from django.shortcuts import render, HttpResponseRedirect,get_object_or_404
from django.contrib import messages
from .models import death, recovery, newcase, deathdetail, testcount,keycountry,indianabroad, feedback
import datetime
import pandas as pd
from math import log
from dash.tables import deathdetailtable,indianabroadtable, statewisedetailtable,indiatable
from django.db.models import F
from data_updater.india_data_maker import mainman
import os
from django.http import JsonResponse
from django.conf import settings 


# Create your views here.

stateslist=['andaman_and_nicobar', 'andhra_pradesh', 'arunachal_pradesh', 'assam', 'bihar', 
            'chandigarh', 'chhattisgarh', 'daman_n_diu', 'delhi', 'dadra_nagar_haveli', 'goa',
             'gujarat', 'himachal_pradesh', 'haryana', 'jharkhand', 'jammu_and_kashmir', 'karnataka', 
             'kerala', 'lakshadeep', 'ladakh', 'maharashtra', 'meghalaya', 'manipur', 'madhya_pradesh', 
             'mizoram', 'nagaland', 'odisha', 'punjab', 'puducherry', 'rajasthan', 'sikkim', 'tamil_nadu', 
             'telangana', 'tripura', 'uttar_pradesh', 'uttarakhand', 'west_bengal'
            ]

stateslist1=['Andaman and Nicobar Island', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 
            'Chandigarh', 'Chhattisgarh', 'Daman and Diu', 'Delhi', 'Dadra and Nagar Haveli', 'Goa',
             'Gujarat', 'Himachal Pradesh', 'Haryana', 'Jharkhand', 'Jammu and Kashmir', 'Karnataka', 
             'kerala', 'Lakshadeep', 'Ladakh', 'Maharashtra', 'Meghalaya', 'Manipur', 'Madhya Pradesh', 
             'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Puducherry', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 
             'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
            ]

#actual mortality may reduce over time as the number of active cases decreases

class resources:
    
    def indiatabledata(request):
        #we need somethin like this
        #{'state':'mh', 'confirmed': '1000','active':'600', 'recovered':'200', 'death':'100'}
        
        context={}
        statedeath=[]
        statenewcase=[]
        staterecovery=[]
        dic={}
        alllist=[]
        context['states']=stateslist
        for state in stateslist:
            dcount=0
            ncount=0
            rcount=0
            for obj in death.objects.all():
                dcount=dcount+getattr(obj, state)
            statedeath.append(dcount)
            for obj in newcase.objects.all():
                ncount=ncount+getattr(obj, state)
            statenewcase.append(ncount)
            for obj in recovery.objects.all():
                rcount=rcount+getattr(obj, state)
            staterecovery.append(rcount)
            
        for i in range(len(stateslist)):
            dic['State']=stateslist1[i]
            dic['T']=statenewcase[i]
            dic['A']=statenewcase[i]-statedeath[i]-staterecovery[i]
            dic['R']=staterecovery[i]
            dic['D']=statedeath[i]
            alllist.append(dic)
            dic={}
            
        
        print(alllist)   
        
        table=indiatable(alllist)
        return table  
        
        
        pass
    
    def dashboard(request):
        context={}
        death_count=0
        case_count=0
        recovery_count=0
        for obj in death.objects.all():
            for i in range(len(stateslist)):
                count=getattr(obj, stateslist[i])
                death_count=count+death_count
                
        for obj in newcase.objects.all():
            for i in range(len(stateslist)):
                count=getattr(obj, stateslist[i])
                case_count=count+case_count
                
        for obj in recovery.objects.all():
            for i in range(len(stateslist)):
                count=getattr(obj, stateslist[i])
                recovery_count=count+recovery_count
        
        active_count=case_count-death_count-recovery_count
        tot_age=0
        count=0
        for obj in deathdetail.objects.all():
            if obj.age<100:
                tot_age=tot_age+obj.age
                count=count+1
                
        avg_age=int(tot_age/count)
        
        tot_test=0
        testdf=pd.read_excel('updated_covid.xlsx', sheet_name='testsdone')
        for i in range(len(testdf)):
            if testdf.iloc[i,1] != 0:
            #print(testdf.iloc[i,1])
                tot_test=testdf.iloc[i,1]
        beds=0.7 #2011 latest worldbank
        docs=0.8 #2017 latest worldbank
        nurses=2.1 #2017 latest worldbank
        
        
        
        beds_old=5.2
        docs_old=5.9
        nurses_old=15.6
        
        #find mortality
        mortality=int((death_count/death_count)*100)
        
        if active_count < (30/100)*case_count:
            context['free_box']=mortality
            context['free_message']="Mortality*"
            context['asterisk']="*The actual mortality may vary as the number of active cases vary"
        else:
            context['free_box']=avg_age
            context['free_message']="Avg age*"
            context['asterisk']="*Avg age of deceased calculated from limited sample of 71"
        context['case_count']=case_count 
        context['death_count']=death_count
        context['recovery_count']=recovery_count
        context['active_count']=active_count
        context['avg_age']=avg_age
        context['beds']=beds
        context['docs']=docs
        context['nurses']=nurses
        context['beds_old']=beds_old
        context['docs_old']=docs_old
        context['nurses_old']=nurses_old
        context['tot_test']=tot_test
        updatetimeobj=death.objects.all()
        for obj in updatetimeobj:
            context['update_time']=obj.datetime_update
        
        
        
        
        
        return context
     
    
    def countrychart(scalelog=False):
        log
        country_dict={}
        i=1
        countrylist=[]
        for obj in keycountry.objects.all():
            day='Day '+str(i)
            ls=[]
            
            ls.extend((obj.china, obj.us, obj.uk,obj.italy, obj.france, obj.germany, obj.spain, obj.iran, obj.india))
            
            if scalelog==True:
                lslog=[log(ele, 10) for ele in ls if ele !=0]
                for item in lslog:
                    if item==0:
                        item=0.000000000000000000000000001
                ls=[]
                ls=lslog
            countrylist.append(ls)
            country_dict[day]=ls
            i=i+1
        chinalist=[]   
        uslist=[]
        uklist=[]
        italylist=[]
        francelist=[]
        germanylist=[]
        spainlist=[]
        iranlist=[]
        indialist=[] 
        
        #only after first 100 switch
        china_switch=False
        us_switch=False
        uk_switch=False
        italy_switch=False
        france_switch=False
        germany_switch=False
        spain_switch=False
        iran_switch=False
        
        
        
        for k, v in country_dict.items():
                        
            if country_dict[k][0] >100:
                chinalist.append(country_dict[k][0])
            if country_dict[k][1] >100:
                uslist.append(country_dict[k][1])
            if country_dict[k][2] >100:
                uklist.append(country_dict[k][2])                
            if country_dict[k][3] >100:
                italylist.append(country_dict[k][3])
            if country_dict[k][4] >100:
                francelist.append(country_dict[k][4])
            if country_dict[k][5] >100:
                germanylist.append(country_dict[k][5])
            if country_dict[k][6] >100:
                spainlist.append(country_dict[k][6])
            if country_dict[k][6] >100:
                iranlist.append(country_dict[k][7])
            if country_dict[k][8] >100:
                indialist.append(country_dict[k][8])
            
        return country_dict, chinalist, uslist, uklist, italylist,francelist, germanylist, spainlist, iranlist, indialist

        
        #print(country_dict)
    
    
    def chartlist(chartmodel):
        
        item_dict={}
        item_count=0
        for obj in chartmodel.objects.all():
            for i in range(len(stateslist)):
                count=getattr(obj, stateslist[i])
                item_count=count+item_count
            date=("{:%b %d}".format(obj.date))
            item_dict[date]=item_count
            item_count=0
        return item_dict
              
    
    def chartscontent(request):
        context={}
        death_dict=resources.chartlist(death,)
        newcase_dict=resources.chartlist(newcase)
        recovery_dict=resources.chartlist(recovery)
        context['death_dict']=death_dict
        context['newcase_dict']=newcase_dict
        context['recovery_dict']=recovery_dict
        
        all_dict={}
        for k, v in death_dict.items():
            ls=[]
            ls.extend((newcase_dict[k],death_dict[k], recovery_dict[k]))
            all_dict[k]=ls
        print(all_dict)
        #print('addlist;',all_dict[datetime.date(2020, 3, 2)][0])
        context['all_dict']=all_dict
        
        country_dict,  chinalist, uslist, uklist, italylist,francelist, germanylist, spainlist, iranlist, indialist=resources.countrychart() 
        context['country_dict']=country_dict
        context['chinalist']=chinalist
        context['uslist']=uslist
        context['uklist']=uklist
        context['italylist']=italylist
        context['francelist']=francelist
        context['germanylist']=germanylist
        context['spainlist']=spainlist
        context['iranlist']=iranlist
        context['indialist']=indialist

        i=1
        trend_dict={}
        # avgls=[]
        # for obj in newcase.objects.all():
        #     ls=[]
        #     ls.append(all_dict[obj.date][0])
        #     avgls.append(all_dict[obj.date][0])
        #     if(len(avgls)>5):
        #         avgtot=0
        #         for item in avgls:
        #             avgtot=((item+avgtot))
        #         avgtot=avgtot/5
        #        # print(avgtot)   
        #         avgls.pop(0)
        #     else:
        #         avgtot=0
        #     ls.append(avgtot)
        #     trend_dict[obj.date]=ls
        #     ls=[]    
            
        # context['trend_dict']=trend_dict
        #print('\n\n trend_dict',trend_dict)
        
        return context
        #area chart number of cases done
        #5 point trail moving avg done
        #log scalse 
        #countrywise data italy, india, spain, southkorea, iran, britan, us done
        
        #select state if required..
        #select  
        
##stacked bar chart

    def stackedbarstate():
        context={}
        statedeath=[]
        statenewcase=[]
        staterecovery=[]
        context['states']=stateslist
        for state in stateslist:
            dcount=0
            ncount=0
            rcount=0
            for obj in death.objects.all():
                dcount=dcount+getattr(obj, state)
            statedeath.append(dcount)
            for obj in newcase.objects.all():
                ncount=ncount+getattr(obj, state)
            statenewcase.append(ncount)
            for obj in recovery.objects.all():
                rcount=rcount+getattr(obj, state)
            staterecovery.append(rcount)
        
        nstateslist=[x for _,x in sorted(zip(statenewcase,stateslist), reverse=True)]
        nstatedeath=[x for _,x in sorted(zip(statenewcase,statedeath), reverse=True)]
        nstaterecovery=[x for _,x in sorted(zip(statenewcase,staterecovery), reverse=True)]
        nstatenewcase=sorted(statenewcase, reverse=True)
        
        nl=[]
        for d, r, n in zip(nstatedeath, nstaterecovery,nstatenewcase):
            n=n-d-r
            nl.append(n)
        nstatenewcase=[]
        nstatenewcase=nl
        qs=zip(stateslist,statedeath,staterecovery,statenewcase)  

        #sor accoring to new cases
        #sort state list accorinig to 
        
        topfive=nstateslist[:5]
        
        context['topfive']=topfive

        context['qs']=qs
        context['stateslist']=nstateslist
        context['statedeath']=nstatedeath
        context['statenewcase']=nstatenewcase
        context['staterecovery']=nstaterecovery
        
        
        
        return context
        
    def topfiveloop(tstate):
        
        count=0
        item_dict={}
        for obj in newcase.objects.all():
            count=count+getattr(obj, tstate)
            date=("{:%b %d}".format(obj.date))
            item_dict[date]=count
        return item_dict
    
    def topfivestate(topfive):
        
        context={}
        #print(topfive)
        context['top1_name']=topfive[0]
        context['top2_name']=topfive[1]
        context['top3_name']=topfive[2]
        context['top4_name']=topfive[3]
        context['top5_name']=topfive[4]
        top1=resources.topfiveloop(topfive[0])
        top2=resources.topfiveloop(topfive[1])
        top3=resources.topfiveloop(topfive[2])
        top4=resources.topfiveloop(topfive[3])
        top5=resources.topfiveloop(topfive[4])
    
       # print(top1, '\n')
       ## print(top2,'\n')
        ##print(top4,'\n')
        #print(top5,'\n')  
        
        context['top1']=top1
        context['top2']=top2
        context['top3']=top3
        context['top4']=top4
        context['top5']=top5
        return context
        
           
def dancingmonkeys(request):
    template='dancingmonkeys.html'
    return render(request, template)

def home(request):  
    
    context={}
    table=resources.indiatabledata(request)
    
    context['table']=table
    context1=resources.dashboard(request)
    if 'India' in request.POST or request.method=='GET':
        context2=resources.chartscontent(request)
    else:
        state=request.POST['state']
        context2=resources.chartscontent(request, state)
    context3=resources.stackedbarstate()
    context4=resources.topfivestate(context3['topfive'])
    context={**context, **context1, **context2, **context3, **context4} #joining two dicts
    qs=context['qs']
    
    
    #top five states trendline
    # 
    # #up, kerala,maharashtra, tamilnadu , delhi...

    #single chart page with state trend ...new .. recovered, and dead...

    #state wise info,
    #trendline for state
    
    #make a script that deletes all and updates new script and saves data...
    #google analytics
    
    
    template='dashboard.html'
    return render(request, template, context)

def deathdetailview(request):
    data=deathdetail.objects.all()
    table=deathdetailtable(data)
    context={}
    context['table']=table
    template='deathdetailview.html'
    
    return render(request, template, context)



def scriptrequest(request, password=None):
    
    print(request.GET)
    print('this is in the request',request.GET['password'])
    try:
        password=request.GET['password']
        if password==settings.RESET_PASS:
            result=update()
            
            return JsonResponse({'Result ':'Done'})
        else:
            return JsonResponse({'Error ':'Wrong Password'})
    except:
        return JsonResponse({'Error':'Wrong request'})
    
    

def statewisedetailview(request):
    context={}
    try:
        state=request.GET['state']
    except:
        state=None
    if state==None:
        state='kerala'
    newcaseqs=newcase.objects.all().order_by('date').annotate(fstate=F(state)).values('date','fstate')
    deathqs=death.objects.all().order_by('date').annotate(fstate=F(state)).values('fstate')
    recoveryqs=recovery.objects.all().order_by('date').annotate(fstate=F(state)).values('fstate')
    #print(newcaseqs)
    
    newdict={}
    ls=[]
    for item in newcaseqs:
        newdict['date']=("{:%b %d}".format(item['date']))
        newdict['new_case']=item['fstate']
        ls.append(newdict)
        newdict={}
    
    i=0
    for item in deathqs:
        newdict=ls[i]
        newdict['deaths']=item['fstate']
        i=i+1
    
    i=0
    for item in recoveryqs:
        newdict=ls[i]   
        newdict['recovery']=item['fstate']
        i=i+1
    
    ##add date in desired format to pass to template
    datelist=[]
    for item in newcaseqs:
        dateobj=("{:%b %d}".format(item['date']))
        datelist.append(dateobj)
        

    table=statewisedetailtable(ls)
    context['place']=state.upper()
    context['newcaseqs']=newcaseqs
    context['deathqs']=deathqs
    context['recoveryqs']=recoveryqs
    context['table']=table
    context['stateslist']=stateslist
    context['datelist']=datelist
    
    template='statewisedetailview.html'
    
    return render(request, template, context)
    
    
        
        
    
    
def indianabroadview(request):
    
    #statewisedetailview(request)
    data=indianabroad.objects.all()
    table=indianabroadtable(data)
    context={}
    context['table']=table
    template='indianabroadview.html'
    
    return render(request, template, context)


def update():
    mainman()
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
    # print(df_abroad)
    entries = []
    for e in df_abroad.T.to_dict().values():
        entries.append(indianabroad(**e))
    for item in entries:
        item.datetime_update=datetime.datetime.now()

    indianabroad.objects.bulk_create(entries)
    
    return True


def reset(request):
    
    
    if request.method=='POST':
        print(request.POST)
        return 'hello'
        
        password=request.POST['password']
        
        if password==settings.RESET_PASS:
            update()
            return HttpResponseRedirect('/')
            
        else:
            messages.info(request, "Incorrect password")  
            return HttpResponseRedirect('reset')
    else:
        return render(request, 'reset.html')
        
def feedbackview(request):
    
    try:
        feedbackitem=request.GET['feedback']
        person=request.GET['person']
    except:
        #print('hello')
        feedbackitem=None
        person=None
        
    if feedbackitem != None and person != None:
        feedback.objects.create(feedback=feedbackitem, person=person, datetime_update=datetime.datetime.now())
        messages.info(request, 'Thank you for your valuable feedback')
        return HttpResponseRedirect('/')
    else:
        template='feedbackview.html'
        return render(request, template)
        
def aboutview(request):
    return render(request, 'aboutview.html')      