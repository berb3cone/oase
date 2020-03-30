from django.shortcuts import render
from django.http import Http404
from main.models import Loan_client
from main.models import Nutrition_client
import numpy as np
from plotly import tools,offline
import plotly.graph_objs as go
from operator import itemgetter
from main.functions import *

import csv
import io
from django.contrib import messages


# Create your views here.

def home(request):
    return render(request, 'home.html', {})

def login(request):
    return render(request, 'login.html', {})

def financial(request):
    return render(request, 'financial.html', {})

def fin_dashboard(request):
    # Statistics
    records = Loan_client.objects.all()
    c1=0
    c2=0
    f=0
    m=0
    o=0
    tb=0
    ob=0
    hok=0
    hnok=0
    v_age = np.zeros(7, dtype=int)
    v_inc = np.zeros(7, dtype=int)
    l_age = ["<20", "20-29", "30-39", "40-49", "50-59", "60-69", "over 70"]
    l_inc = ["<2000", "2000-2999", "3000-3999", "4000-4999", "5000-5999", "6000-6999", "over 7000"]
    for obj in records:
        if "yes" in obj.pre_approved:
            c1+=1
        else:
            c2+=1
        if "m" in obj.sex:
            m+=1
        elif "f" in obj.sex:
            f+=1
        else:
            o+=1
        if obj.age<20:
            v_age[0]+=1
        elif (obj.age//10)<7:
            v_age[obj.age//10-1]+=1
        else:
            v_age[6]+=1
        if "this" in obj.receiving_income:
            tb+=1
        else:
            ob+=1
        if "not" in obj.loan_history:
            hnok+=1
        else:
            hok+=1
        if obj.net_income<2000:
            v_inc[0]+=1
        elif (obj.net_income//1000)<7:
            v_inc[obj.net_income//1000-1]+=1
        else:
            v_inc[6]+=1


    # Create figure with 6 subplots
    fig = tools.make_subplots(rows=3, cols=2, subplot_titles=('Approval status', 'Loan history', 'Clients age',
                                                              'Clients gender', 'Net income', 'Receiving income'))
    # Add traces
    fig.add_trace(go.Bar(x=["approved", "not approved"], y=[c1, c2], name='applications'), row=1, col=1)
    fig.add_trace(go.Bar(x=["ok", "not ok"], y=[hok, hnok], name='applications'), row=1, col=2)
    fig.add_trace(go.Bar(x=l_age, y=v_age, name='customer/s'), row=2, col=1)
    fig.add_trace(go.Bar(x=["male", "female","other"], y=[m,f,o], name='customer/s'), row=2, col=2)
    fig.add_trace(go.Bar(x=l_inc, y=v_inc, name='customer/s'), row=3, col=1)
    fig.add_trace(go.Bar(x=["at this bank","at other bank"], y=[tb,ob], name='customer/s'), row=3, col=2)

    # Customize title
    # fig.layout.title = 'General statistics'
    # Customize global font family
    fig.layout.font.family = 'Rockwell'
    # Hide legend
    fig.layout.showlegend = False
    # Size
    fig.layout.height = 500

    graph_div = offline.plot(fig, auto_open=False, output_type="div")
    return render(request, 'fin_dashboard.html', {'graph_div': graph_div})

def fin_dashboard2(request):
    # Statistics
    records = Loan_client.objects.all()
    dates_all = []
    dates_app = []
    cont = []
    v_loan = np.zeros(6, dtype=int)
    v_y_loan = np.zeros(6, dtype=int)
    v2_loan=[]
    l_loan = ["<10k", "10k-20k", "20k-30k", "30k-40k", "40k-50k", "over 50k"]

    for obj in records:
        dates_all.append(obj.loan_req_date)
        if "yes" in obj.pre_approved:
            dates_app.append(obj.loan_req_date)
            cont.append([obj.loan_req_date, obj.needed_loan, obj.loan_cost])
        if obj.needed_loan<10000:
            v_loan[0]+=1
            v_y_loan[0]+=obj.return_period
        elif (obj.needed_loan//10000)<5:
            v_loan[obj.needed_loan//10000]+=1
            v_y_loan[obj.needed_loan//10000] += obj.return_period
        else:
            v_loan[5]+=1
            v_y_loan[5] += obj.return_period
    d1=sorted(list(set(dates_all)))
    d2=sorted(list(set(dates_app)))
    s_cont = sorted(cont, key=itemgetter(0))
    c1 = []
    c2 = []
    b_m = []
    r_m = []
    prof = []
    for i in d1:
        c1.append(dates_all.count(i))
    for i in d2:
        c2.append(dates_app.count(i))
        s1=0
        s2=0
        for j in s_cont:
            if i==j[0]:
                s1+=j[1]
                s2+=j[2]
        b_m.append(s1//100*100)
        r_m.append(s2//100*100)
        prof.append((s2//100*100)-(s1//100*100))

    for i in range(6):
        v2_loan.append(round(v_y_loan[i]/v_loan[i],1))

    # Create figure with 3 subplots
    fig = tools.make_subplots(rows=3, cols=1, subplot_titles=('Daily approval', 'Borrowed vs Payback', 'Loan value vs return period'))
    # Add traces
    fig.add_trace(go.Scatter(x=d1, y=c1, name='app received'), row=1, col=1)
    fig.add_trace(go.Scatter(x=d2, y=c2, name='app approved'), row=1, col=1)
    fig.add_trace(go.Scatter(x=d1, y=b_m, name='RON borrowed '), row=2, col=1)
    fig.add_trace(go.Scatter(x=d1, y=r_m, name='RON payback'), row=2, col=1)
    fig.add_trace(go.Bar(x=d1, y=prof, name='RON interest'), row=2, col=1)
    fig.add_trace(go.Bar(x=l_loan, y=v_loan, name='loans'), row=3, col=1)
    fig.add_trace(go.Scatter(x=l_loan, y=v2_loan, name='years'), row=3, col=1)

    # Customize title
    # fig.layout.title = 'Detailed statistics'
    # Customize global font family
    fig.layout.font.family = 'Rockwell'
    # Size
    fig.layout.height = 700

    graph_div = offline.plot(fig, auto_open=False, output_type="div")
    return render(request, 'fin_dashboard2.html', {'graph_div': graph_div})

def health_dashboard(request):
    # Statistics
    records = Nutrition_client.objects.all()

    gender=np.zeros(3, dtype=int)
    v_m_age = np.zeros(7, dtype=int)
    v_f_age = np.zeros(7, dtype=int)
    v_o_age = np.zeros(7, dtype=int)
    v_m_diet = np.zeros(3, dtype=int)
    v_f_diet = np.zeros(3, dtype=int)
    v_o_diet = np.zeros(3, dtype=int)
    v_m_stress = np.zeros(3, dtype=int)
    v_f_stress = np.zeros(3, dtype=int)
    v_o_stress = np.zeros(3, dtype=int)
    v_m_workout = np.zeros(3, dtype=int)
    v_f_workout = np.zeros(3, dtype=int)
    v_o_workout = np.zeros(3, dtype=int)
    l_age = ["<20", "20-29", "30-39", "40-49", "50-59", "60-69", "over 70"]
    l_diet = ["low fat","low carbs","both"]
    l_stress = ["low","medium","high"]
    l_workout = ["once/week","twice/week","more"]

    for obj in records:
        if 'm' in obj.sex:
            gender[0]+=1
            v_m_age[age_interval_calc(obj.age)]+=1
            v_m_diet[diet_calc(obj.diet)] += 1
            v_m_stress[stress_calc(obj.avg_stress_level)] += 1
            v_m_workout[work_calc(obj.workout)] += 1
        elif 'f' in obj.sex:
            gender[1]+=1
            v_f_age[age_interval_calc(obj.age)] += 1
            v_f_diet[diet_calc(obj.diet)] += 1
            v_f_stress[stress_calc(obj.avg_stress_level)] += 1
            v_f_workout[work_calc(obj.workout)] += 1
        else:
            gender[2]+=1
            v_o_age[age_interval_calc(obj.age)] += 1
            v_o_diet[diet_calc(obj.diet)] += 1
            v_o_stress[stress_calc(obj.avg_stress_level)] += 1
            v_o_workout[work_calc(obj.workout)] += 1

    # Create figure with 6 subplots
    fig = tools.make_subplots(rows=3, cols=2, subplot_titles=('Clients gender', 'Age by gender', 'Diet by gender',
                                                              'Stress by gender','Workout by gender'))
    # Add traces
    fig.add_trace(go.Bar(x=["male","female","other"], y=gender, name='client/s'), row=1, col=1)
    fig.add_trace(go.Bar(x=l_age, y=v_m_age, name='m'), row=1, col=2)
    fig.add_trace(go.Bar(x=l_age, y=v_f_age, name='f'), row=1, col=2)
    fig.add_trace(go.Bar(x=l_age, y=v_o_age, name='o'), row=1, col=2)
    fig.add_trace(go.Bar(x=l_diet, y=v_m_diet, name='m'), row=2, col=1)
    fig.add_trace(go.Bar(x=l_diet, y=v_f_diet, name='f'), row=2, col=1)
    fig.add_trace(go.Bar(x=l_diet, y=v_o_diet, name='o'), row=2, col=1)
    fig.add_trace(go.Bar(x=l_stress, y=v_m_stress, name='m'), row=2, col=2)
    fig.add_trace(go.Bar(x=l_stress, y=v_f_stress, name='f'), row=2, col=2)
    fig.add_trace(go.Bar(x=l_stress, y=v_o_stress, name='o'), row=2, col=2)
    fig.add_trace(go.Bar(x=l_workout, y=v_m_workout, name='m'), row=3, col=1)
    fig.add_trace(go.Bar(x=l_workout, y=v_f_workout, name='f'), row=3, col=1)
    fig.add_trace(go.Bar(x=l_workout, y=v_o_workout, name='o'), row=3, col=1)

    # Customize title
    # fig.layout.title = 'General statistics'
    # Customize global font family
    fig.layout.font.family = 'Rockwell'
    # Hide legend
    # fig.layout.showlegend = False
    # Size
    fig.layout.height = 700

    graph_div = offline.plot(fig, auto_open=False, output_type="div")
    return render(request, 'health_dashboard.html', {'graph_div': graph_div})

def health_dashboard2(request):
    # Statistics
    records = Nutrition_client.objects.all()
    ma = [[], [], []]
    m1 = [[], [], []]
    m2 = [[], [], []]
    fa = [[], [], []]
    f1 = [[], [], []]
    f2 = [[], [], []]

    for obj in records:
        if "m" in obj.sex:
            ma[diet_calc(obj.diet)].append(obj.age)
            m1[diet_calc(obj.diet)].append(obj.weight_lost_1)
            m2[diet_calc(obj.diet)].append(obj.weight_lost_2)
        elif "f" in obj.sex:
            fa[diet_calc(obj.diet)].append(obj.age)
            f1[diet_calc(obj.diet)].append(obj.weight_lost_1)
            f2[diet_calc(obj.diet)].append(obj.weight_lost_2)

    # Create figure with 6 subplots
    fig = tools.make_subplots(rows=3, cols=2, subplot_titles=('Men + low fat', 'Women + low fat', 'Men + low carbs',
                                                              'Women + low carbs', 'Men + both', 'Women + both'))
    # Add traces
    fig.add_trace(go.Bar(x=ma[0], y=m1[0], name='1 month',), row=1, col=1)
    fig.add_trace(go.Bar(x=ma[0], y=m2[0], name='3 months'), row=1, col=1)
    fig.add_trace(go.Bar(x=fa[0], y=f1[0], name='1 month', ), row=1, col=2)
    fig.add_trace(go.Bar(x=fa[0], y=f2[0], name='3 months'), row=1, col=2)
    fig.add_trace(go.Bar(x=ma[1], y=m1[1], name='1 month', ), row=2, col=1)
    fig.add_trace(go.Bar(x=ma[1], y=m2[1], name='3 months'), row=2, col=1)
    fig.add_trace(go.Bar(x=fa[1], y=f1[1], name='1 month', ), row=2, col=2)
    fig.add_trace(go.Bar(x=fa[1], y=f2[1], name='3 months'), row=2, col=2)
    fig.add_trace(go.Bar(x=ma[2], y=m1[2], name='1 month', ), row=3, col=1)
    fig.add_trace(go.Bar(x=ma[2], y=m2[2], name='3 months'), row=3, col=1)
    fig.add_trace(go.Bar(x=fa[2], y=f1[2], name='1 month', ), row=3, col=2)
    fig.add_trace(go.Bar(x=fa[2], y=f2[2], name='3 months'), row=3, col=2)


    # Customize title
    # fig.layout.title = 'General statistics'
    # Customize global font family
    fig.layout.font.family = 'Rockwell'
    # Hide legend
    # fig.layout.showlegend = False
    # Size
    fig.layout.height = 700

    graph_div = offline.plot(fig, auto_open=False, output_type="div")
    return render(request, 'health_dashboard2.html', {'graph_div': graph_div})

def health_dashboard3(request):
    # Statistics
    records = Nutrition_client.objects.all()
    ma = [[], [], []]
    m1 = [[], [], []]
    m2 = [[], [], []]
    fa = [[], [], []]
    f1 = [[], [], []]
    f2 = [[], [], []]

    for obj in records:
        if "m" in obj.sex:
            ma[work_calc(obj.workout)].append(obj.age)
            m1[work_calc(obj.workout)].append(obj.weight_lost_1)
            m2[work_calc(obj.workout)].append(obj.weight_lost_2)
        elif "f" in obj.sex:
            fa[work_calc(obj.workout)].append(obj.age)
            f1[work_calc(obj.workout)].append(obj.weight_lost_1)
            f2[work_calc(obj.workout)].append(obj.weight_lost_2)

    # Create figure with 6 subplots
    fig = tools.make_subplots(rows=3, cols=2, subplot_titles=('Men + once/week', 'Women + once/week', 'Men + twice/week',
                                                              'Women + twice/week', 'Men + more', 'Women + more'))
    # Add traces
    fig.add_trace(go.Bar(x=ma[0], y=m1[0], name='1 month',), row=1, col=1)
    fig.add_trace(go.Bar(x=ma[0], y=m2[0], name='3 months'), row=1, col=1)
    fig.add_trace(go.Bar(x=fa[0], y=f1[0], name='1 month', ), row=1, col=2)
    fig.add_trace(go.Bar(x=fa[0], y=f2[0], name='3 months'), row=1, col=2)
    fig.add_trace(go.Bar(x=ma[1], y=m1[1], name='1 month', ), row=2, col=1)
    fig.add_trace(go.Bar(x=ma[1], y=m2[1], name='3 months'), row=2, col=1)
    fig.add_trace(go.Bar(x=fa[1], y=f1[1], name='1 month', ), row=2, col=2)
    fig.add_trace(go.Bar(x=fa[1], y=f2[1], name='3 months'), row=2, col=2)
    fig.add_trace(go.Bar(x=ma[2], y=m1[2], name='1 month', ), row=3, col=1)
    fig.add_trace(go.Bar(x=ma[2], y=m2[2], name='3 months'), row=3, col=1)
    fig.add_trace(go.Bar(x=fa[2], y=f1[2], name='1 month', ), row=3, col=2)
    fig.add_trace(go.Bar(x=fa[2], y=f2[2], name='3 months'), row=3, col=2)


    # Customize title
    # fig.layout.title = 'General statistics'
    # Customize global font family
    fig.layout.font.family = 'Rockwell'
    # Hide legend
    # fig.layout.showlegend = False
    # Size
    fig.layout.height = 700

    graph_div = offline.plot(fig, auto_open=False, output_type="div")
    return render(request, 'health_dashboard3.html', {'graph_div': graph_div})

def loan_app_list(request):
    records = Loan_client.objects.all()
    return render(request, 'loan_app_list.html', {'entryS': records})

def form_detail(request, id):
    try:
        myID = Loan_client.objects.get(id=id)
    # except Exception as e:
    #     return e
    except:
        raise Http404("Currently there is no entry with this name in the database.")
    else:
        return render(request,'loan_form_detail.html',{'myID':myID})

def health(request):
    return render(request, 'health.html', {})

def nutr_cli_list(request):
    records = Nutrition_client.objects.all()
    return render(request, 'nutr_cli_list.html', {'entryS': records})

def nutr_detail(request, id):
    try:
        myID = Nutrition_client.objects.get(id=id)
    # except Exception as e:
    #     return e
    except:
        raise Http404("Currently there is no entry with this name in the database.")
    else:
        return render(request,'nutr_detail.html',{'myID':myID})

def contact(request):
    return render(request, 'contact.html', {})


def add_loan_clients(request):

    if request.method =='GET':
        return render(request, 'add_loan_clients.html', {})

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Loan_client.objects.update_or_create(
            first_name=column[0],
            last_name=column[1],
            receiving_income=column[2],
            email=column[3],
            sex=column[4],
            loan_history=column[5],
            birth_date=column[6],
            education=column[7],
            work_experience=column[8],
            gross_income=column[9],
            tax_percent=column[10],
            dependents=column[11],
            current_monthly_payments=column[12],
            loan_req_date=column[13],
            needed_loan=column[14],
            return_period=column[15]
        )
        return render(request, 'add_loan_clients.html', {})












