from django.shortcuts import render, redirect
from django.db.models import sql
from django.conf import settings
from django.http import HttpResponse , Http404
from django.contrib.auth.forms import UserCreationForm
from .models import Disease_Model,Personal_Species_Model,Job_History_Model,Assessment_Model,Personal_History_Model,Examinations_Model,Experiments_Model,Para_Clinic_Model,Consulting_Model,Final_Theory_Model,ExaminationsCourse
from .forms import submit_company_form,registration,disease_form,personal_species_form,job_history_form,assessment_form,personal_history_form,examinations_form,experiments_form,para_clinic_form,consulting_form,final_theory_form,submit_course_form
from django.contrib import messages
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.views.decorators.http import require_POST
from django.views import generic
from . import forms, models
from django.core.paginator import Paginator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from django.templatetags.static import static
from shutil import move
import os
from fpdf import FPDF
from time import sleep
from PIL import Image


def home_view(request):
    return render(request, 'home.html')
    

def contact_us_view(request):
    return render(request, 'contact_us.html')


def occupational_medicine_view(request):
    return render(request, 'occupational_medicine.html')


def services_view(request):
    return render(request, 'services.html')


def register_view(request):
    form = registration()
    if request.method == 'POST':
        form = registration(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'account made succcessfuly for ' + user)
            return redirect('../login')
    context = {'form': form}
    return render(request, 'register.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorect')
    return render(request, 'login.html')




# @login_required(login_url='login')
# def submit_person_view(request):
#     work=Summary_Of_Results_Model.objects.last()
#     code_list=Submit_Company_Model.objects.order_by('id')
#     if work:
#         code=work.examinations_code
#     else:
#         code=''
#     initial_dict = {
#         'examinations_code':code
        
#     }

#     form=summary_of_results_form(initial=initial_dict)
#     context={'form':form,
#     'code_list':code_list}
#     return render(request,'examinations.html',context)


# @require_POST
# def addperson_view(request):
#     form = summary_of_results_form(request.POST)
#     if form.is_valid():
#         new_summary = form.save()
#     return redirect('submit_person')


def logoutuser_view(request):
    logout(request)
    return redirect('../')


@login_required(login_url='login')
def submit_course_view(request):
    form=submit_course_form()
    context={'form':form}
    return render(request, 'submit_course.html',context)


@require_POST
def addcourse_view(request):
    form=submit_course_form(request.POST)
    if form.is_valid():
        course_form = form.save(commit=False)
        course_form.examinations_code = str(course_form.company) + str(course_form.year)
        course_form.save()
    return redirect('submit_course')


@login_required(login_url='login')
def submit_company_view(request):
    form=submit_company_form()
    context={'form':form}
    return render(request, 'submit_company.html',context)


@require_POST
def addcompany_view(request):
    form=submit_company_form(request.POST)
    if form.is_valid():
        new_company=form.save()
    return redirect('submit_company')

@login_required(login_url='login')
def output_view(request):
    form=disease_form()
    code_list=ExaminationsCourse.objects.order_by('id')
    context={'form':form,'code_list':code_list}
    return render(request,'output.html',context)

@require_POST
def adddisease_view(request):
    if Disease_Model:
        model=Disease_Model.objects.last()
    else:
        a = Disease_Model(examinations_code='',order_number=1)
        a.save()
        model=Disease_Model.objects.last()
    form=disease_form(request.POST)
    if form.is_valid():
        model.examinations_code=form.cleaned_data['examinations_code']
        model.save()
    return redirect('output')

@require_POST
def addexaminations_output_person_addn_view(request):
    if Disease_Model:
        model=Disease_Model.objects.last()
    else:
        a = Disease_Model(examinations_code='',order_number=1)
        a.save()
        model=Disease_Model.objects.last()
    form=disease_form(request.POST)
    if form.is_valid():
        if not form.cleaned_data['p_fathers_name']:
            form.cleaned_data['p_fathers_name'] = 'None'
        if not form.cleaned_data['p_personal_code']:
            form.cleaned_data['p_personal_code'] = 0
        model.p_name=form.cleaned_data['p_name']
        model.p_fathers_name=form.cleaned_data['p_fathers_name']
        model.p_age=form.cleaned_data['p_age']
        model.p_personal_code=form.cleaned_data['p_personal_code']
        model.save()
    return redirect('examinations_output_person')

@require_POST
def addexaminations_output_person_addex_view(request):
    if Disease_Model:
        model=Disease_Model.objects.last()
    else:
        a = Disease_Model(examinations_code='',order_number=1)
        a.save()
        model=Disease_Model.objects.last()
    form=disease_form(request.POST)
    if form.is_valid():
        model.p_examinations_code=form.cleaned_data['p_examinations_code']
        model.save()
    return redirect('examinations_output_person')


@login_required(login_url='login')
def disease_code_view(request):
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    job_history=Job_History_Model.objects.all()
    assessment=Assessment_Model.objects.all()
    personal_history=Personal_History_Model.objects.all()
    examinations=Examinations_Model.objects.all()
    experiments=Experiments_Model.objects.all()
    para_clinic=Para_Clinic_Model.objects.all()
    consulting=Consulting_Model.objects.all()
    final_theory=Final_Theory_Model.objects.all()
    context={'personal_species' : personal_species , 'job_history' : job_history , 'assessment' : assessment, 'personal_history' : personal_history, 'examinations' : examinations, 'experiments' : experiments, 'para_clinic' : para_clinic, 'consulting' : consulting , 'final_theory' : final_theory, 'examinations_course':examinations_course}
    return render(request, 'disease_code.html',context)


def disease_pdf_view(request):
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    options = Options()
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get("http://www.parsianqom.ir/login")
    username = driver.find_element('name',"username")
    password = driver.find_element('name',"password")
    login_but = driver.find_element('name',"login")
    username.send_keys('bot')
    password.send_keys('botamiri84')
    login_but.click()
    driver.get("http://www.parsianqom.ir/output/disease_code")
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(1920,S('Height'))
    count = 0
    i = 0
    if personal_species:
        for n in personal_species:
            count += 1
        n = count
        count = count // 20
        if i % 20 != 0:
            count += 1
        pdf = FPDF()
        while i <= count :
            if i == count:
                height = (n - (count * 20) + 1) * 7.14
                WebDriverWait(driver, 10000).until(
                EC.presence_of_element_located((By.ID,'disease' + str(i)))).screenshot('images/'+ str(i) +'disease.png')
                WebDriverWait(driver, 10000).until(
                EC.presence_of_element_located((By.ID, "Head"))).screenshot('images/Head.png')
                pdf.add_page()
                pdf.image('images/Head.png',-1,None,220,20)
                pdf.image('images/'+ str(i) +'disease.png',3,None,205,height)
                os.remove('images/'+ str(i) +'disease.png')
                os.remove('images/Head.png')
                i += 1
            else:
                WebDriverWait(driver, 10000).until(
                EC.presence_of_element_located((By.ID,'disease' + str(i)))).screenshot('images/'+ str(i) +'disease.png')
                WebDriverWait(driver, 10000).until(
                EC.presence_of_element_located((By.ID, "Head"))).screenshot('images/Head.png')
                pdf.add_page()
                pdf.image('images/Head.png',-1,None,220,20)
                pdf.image('images/'+ str(i) +'disease.png',3,None,205,150)
                os.remove('images/'+ str(i) +'disease.png')
                os.remove('images/Head.png')
                i += 1
    else:
        pdf = FPDF()
        pdf.add_page()
    pdf.output("pdfs/disease.pdf", "F")
    file_path = os.path.join('pdfs/disease.pdf')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required(login_url='login')
def open_docs_view(request):
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course,final__mashrot='False',final__belamane='False',final__rad='False')
    job_history=Job_History_Model.objects.all()
    assessment=Assessment_Model.objects.all()
    personal_history=Personal_History_Model.objects.all()
    examinations=Examinations_Model.objects.all()
    experiments=Experiments_Model.objects.all()
    para_clinic=Para_Clinic_Model.objects.all()
    consulting=Consulting_Model.objects.all()
    final_theory=Final_Theory_Model.objects.all()
    context={'personal_species' : personal_species , 'job_history' : job_history , 'assessment' : assessment, 'personal_history' : personal_history, 'examinations' : examinations, 'experiments' : experiments, 'para_clinic' : para_clinic, 'consulting' : consulting , 'final_theory' : final_theory , 'examinations_course':examinations_course}
    return render(request, 'open_docs.html',context)


def open_docs_pdf_view(request):
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course,final__mashrot='False',final__belamane='False',final__rad='False')
    options = Options()
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get("http://www.parsianqom.ir/login")
    username = driver.find_element('name',"username")
    password = driver.find_element('name',"password")
    login_but = driver.find_element('name',"login")
    username.send_keys('bot')
    password.send_keys('botamiri84')
    login_but.click()
    driver.get("http://www.parsianqom.ir/output/open_docs")
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(1920,S('Height'))
    count = 0
    i = 0
    if personal_species:
        for n in personal_species:
            count += 1
        n = count
        count = count // 20
        if i % 20 != 0:
            count += 1
        pdf = FPDF()
        while i <= count :
            if i == count:
                height = (n - (count * 20) + 1) * 7.14
                driver.find_element('id','open' + str(i)).screenshot('images/'+ str(i) +'open.png')
                driver.find_element('id','Head').screenshot('images/Head.png')
                pdf.add_page()
                pdf.image('images/Head.png',-1,None,220,20)
                pdf.image('images/'+ str(i) +'open.png',3,None,205,height)
                os.remove('images/'+ str(i) +'open.png')
                os.remove('images/Head.png')
                i += 1
            else:
                driver.find_element('id','open' + str(i)).screenshot('images/'+ str(i) +'open.png')
                driver.find_element('id','Head').screenshot('images/Head.png')
                pdf.add_page()
                pdf.image('images/Head.png',-1,None,220,20)
                pdf.image('images/'+ str(i) +'open.png',3,None,205,150)
                os.remove('images/'+ str(i) +'open.png')
                os.remove('images/Head_img.png')
                i += 1
    else:
        pdf = FPDF()
        pdf.add_page()
    pdf.output("pdfs/open.pdf", "F")
    file_path = os.path.join('pdfs/open.pdf')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required(login_url='login')
def summary_of_examinations_view(request):
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    job_history=Job_History_Model.objects.all()
    assessment=Assessment_Model.objects.all()
    personal_history=Personal_History_Model.objects.all()
    examinations=Examinations_Model.objects.all()
    experiments=Experiments_Model.objects.all()
    para_clinic=Para_Clinic_Model.objects.all()
    consulting=Consulting_Model.objects.all()
    final_theory=Final_Theory_Model.objects.all()
    context={'personal_species' : personal_species , 'job_history' : job_history , 'assessment' : assessment, 'personal_history' : personal_history, 'examinations' : examinations, 'experiments' : experiments, 'para_clinic' : para_clinic, 'consulting' : consulting , 'final_theory' : final_theory , 'examinations_course':examinations_course}
    return render(request, 'summary_of_examinations.html',context)



def summary_of_examinations_pdf_view(request):
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    options = Options()
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get("http://www.parsianqom.ir/login")
    username = driver.find_element('name',"username")
    password = driver.find_element('name',"password")
    login_but = driver.find_element('name',"login")
    username.send_keys('bot')
    password.send_keys('botamiri84')
    login_but.click()
    driver.get("http://www.parsianqom.ir/output/summary_of_examinations")
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(1920,S('Height'))
    count = 0
    i = 0
    if personal_species:
        for n in personal_species:
            count += 1
        n = count
        count = count // 20
        if i % 20 != 0:
            count += 1
        pdf = FPDF()
        while i <= count :
            if i == count:
                height = (n - (count * 20) + 1) * 17
                driver.find_element('id','summary' + str(i)).screenshot('images/'+ str(i) +'summary.png')
                driver.find_element('id','Head').screenshot('images/Head.png')
                pdf.add_page()
                pdf.image('images/Head.png',-1,None,220,20)
                pdf.image('images/'+ str(i) +'summary.png',3,None,205,height)
                os.remove('images/'+ str(i) +'summary.png')
                os.remove('images/Head.png')
                i += 1
            else:
                height = (20) * 17
                driver.find_element('id','summary' + str(i)).screenshot('images/'+ str(i) +'summary.png')
                driver.find_element('id','Head').screenshot('images/Head.png')
                pdf.add_page()
                pdf.image('images/Head.png',-1,None,220,20)
                pdf.image('images/'+ str(i) +'summary.png',3,None,205,height)
                os.remove('images/'+ str(i) +'summary.png')
                os.remove('images/Head.png')
                i += 1
    else:
        pdf = FPDF()
        pdf.add_page()
    pdf.output("pdfs/summary.pdf", "F")
    file_path = os.path.join('pdfs/summary.pdf')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required(login_url='login')
def problem_view(request):
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    job_history=Job_History_Model.objects.all()
    assessment=Assessment_Model.objects.all()
    personal_history=Personal_History_Model.objects.all()
    examinations=Examinations_Model.objects.all()
    experiments=Experiments_Model.objects.all()
    para_clinic=Para_Clinic_Model.objects.all()
    consulting=Consulting_Model.objects.all()
    final_theory=Final_Theory_Model.objects.all()
    context={'personal_species' : personal_species , 'job_history' : job_history , 'assessment' : assessment, 'personal_history' : personal_history, 'examinations' : examinations, 'experiments' : experiments, 'para_clinic' : para_clinic, 'consulting' : consulting , 'final_theory' : final_theory,'examinations_course':examinations_course}
    return render(request, 'problem.html',context)
def problem_pdf_view(request):
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    options = Options()
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get("http://www.parsianqom.ir/login")
    username = driver.find_element('name',"username")
    password = driver.find_element('name',"password")
    login_but = driver.find_element('name',"login")
    username.send_keys('bot')
    password.send_keys('botamiri84')
    login_but.click()
    driver.get("http://www.parsianqom.ir/output/problem")
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(1920,S('Height'))
    count = 0
    i = 0
    if personal_species:
        for n in personal_species:
            count += 1
        n = count
        count = count // 20
        if i % 20 != 0:
            count += 1
        pdf = FPDF()
        while i <= count :
            if i == count:
                height = (n - (count * 20) + 1) * 7.14
                driver.find_element('id','problem' + str(i)).screenshot('images/'+ str(i) +'problem.png')
                driver.find_element('id','Head').screenshot('images/Head.png')
                pdf.add_page()
                pdf.image('images/Head.png',-1,None,220,20)
                pdf.image('images/'+ str(i) +'problem.png',3,None,205,height)
                os.remove('images/'+ str(i) +'problem.png')
                os.remove('images/Head.png')
                i += 1
            else:
                driver.find_element('id','problem' + str(i)).screenshot('images/'+ str(i) +'problem.png')
                driver.find_element('id','Head').screenshot('images/Head.png')
                pdf.add_page()
                pdf.image('images/Head.png',-1,None,220,20)
                pdf.image('images/'+ str(i) +'problem.png',3,None,205,150)
                os.remove('images/'+ str(i) +'problem.png')
                os.remove('images/Head.png')
                i += 1
    else:
        pdf = FPDF()
        pdf.add_page()
    pdf.output("pdfs/problem.pdf", "F")
    file_path = os.path.join('pdfs/problem.pdf')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
@login_required(login_url='login')
def specialist_view(request):
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    job_history=Job_History_Model.objects.all()
    assessment=Assessment_Model.objects.all()
    personal_history=Personal_History_Model.objects.all()
    examinations=Examinations_Model.objects.all()
    experiments=Experiments_Model.objects.all()
    para_clinic=Para_Clinic_Model.objects.all()
    consulting=Consulting_Model.objects.all()
    final_theory=Final_Theory_Model.objects.all()
    context={'personal_species' : personal_species , 'job_history' : job_history , 'assessment' : assessment, 'personal_history' : personal_history, 'examinations' : examinations, 'experiments' : experiments, 'para_clinic' : para_clinic, 'consulting' : consulting , 'final_theory' : final_theory,'examinations_course':examinations_course}
    return render(request, 'specialist.html',context)

@login_required(login_url='login')
def graph_view(request):
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    a_tri,b_tri,c_tri=0,0,0
    data_tri=[]
    a_chl,b_chl,c_chl=0,0,0
    data_chl=[]
    a_sug,b_sug,c_sug,d_sug=0,0,0,0
    data_sug=[]
    a_pre,b_pre,c_pre,d_pre=0,0,0,0
    data_pre=[]
    a_ry,b_ry,c_ry=0,0,0
    data_ry=[]
    a_ly,b_ly,c_ly=0,0,0
    data_ly=[]
    a_esp,b_esp,c_esp,d_esp,e_esp,f_esp=0,0,0,0,0,0
    data_esp=[]
    a_rg,b_rg,c_rg,d_rg,e_rg,f_rg=0,0,0,0,0,0
    data_rg=[]
    a_lg,b_lg,c_lg,d_lg,e_lg,f_lg=0,0,0,0,0,0
    data_lg=[]
    a_u,b_u,c_u=0,0,0
    data_u=[]
    a_p,b_p,c_p,e_p=0,0,0,0,
    data_p=[]
    a_s,b_s,c_s,d_s=0,0,0,0
    data_s=[]
    a_psa,b_psa,c_psa=0,0,0
    data_psa=[]
    a_n,b_n,c_n,d_n,e_n=0,0,0,0,0
    data_n=[]
    a_d,b_d,c_d,d_d,e_d=0,0,0,0,0
    data_d=[]
    count=0
    for summary in personal_species:
        count+=1
        experiments=Experiments_Model.objects.filter(person=summary).last()
        if not experiments.tg:
            c_tri += 1
        elif experiments.tg_status == False:
            b_tri += 1
        else:
            a_tri += 1    
    data_tri.append(a_tri)
    data_tri.append(b_tri)
    data_tri.append(c_tri)


    for summary in personal_species:
        experiments=Experiments_Model.objects.filter(person=summary).last()
        if not experiments.chol:
            c_chl += 1
        elif experiments.chol_status == False:
            b_chl += 1
        else:
            a_chl += 1   
    data_chl.append(a_chl)
    data_chl.append(b_chl)
    data_chl.append(c_chl)


    for summary in personal_species:
        experiments=Experiments_Model.objects.filter(person=summary).last()
        if experiments.fbs ==  None:
            d_sug += 1   
        elif experiments.fbs < 100:
            a_sug += 1
        elif experiments.fbs < 126:
            b_sug += 1
        elif experiments.fbs >=126:
            c_sug += 1  
    data_sug.append(a_sug)
    data_sug.append(b_sug)
    data_sug.append(c_sug)
    data_sug.append(d_sug)

    for summary in personal_species:
        examinations=Examinations_Model.objects.filter(person=summary).last()
        if examinations.blood_pressure == None:
            d_pre += 1
        elif examinations.blood_pressure < 90:
            c_pre += 1
        elif examinations.blood_pressure >= 90 and examinations.blood_pressure <= 140:
            a_pre += 1
        elif examinations.blood_pressure > 140:
            b_pre += 1
    data_pre.append(a_pre)
    data_pre.append(b_pre)
    data_pre.append(c_pre)
    data_pre.append(d_pre)  



    for summary in personal_species:
        para=Para_Clinic_Model.objects.filter(person=summary).last()
        if para.opto_hedat_r_bi:
            if para.opto_hedat_r_bi == 10:
                a_ry += 1  
            else:
                b_ry += 1
        elif para.opto_hedat_r_status == 'fc' or para.opto_hedat_r_status == 'adam_did':
            b_ry += 1
        else:
            c_ry += 1 
    data_ry.append(a_ry)
    data_ry.append(b_ry)
    data_ry.append(c_ry)


    for summary in personal_species:
        para=Para_Clinic_Model.objects.filter(person=summary).last()
        if para.opto_hedat_l_bi:
            if para.opto_hedat_l_bi == 10:
                a_ly += 1  
            else:
                b_ly += 1
        elif para.opto_hedat_l_status == 'fc' or para.opto_hedat_l_status == 'adam_did':
            b_ly += 1
        else:
            c_ly += 1 
    data_ly.append(a_ly)
    data_ly.append(b_ly)
    data_ly.append(c_ly)


    for summary in personal_species:
        para=Para_Clinic_Model.objects.filter(person=summary).last()
        if para.espiro_tafsir == 'normal':
            a_esp += 1
        elif para.espiro_tafsir == 'tahdidi':
            b_esp += 1
        elif para.espiro_tafsir == 'ensedadi':
            c_esp += 1
        elif para.espiro_tafsir == 'again':
            d_esp += 1
        elif para.espiro_tafsir == 'namaie_toaman':
            e_esp += 1
        elif para.espiro_tafsir == None:
            f_esp += 1
    data_esp.append(a_esp)
    data_esp.append(b_esp)
    data_esp.append(c_esp)
    data_esp.append(d_esp) 
    data_esp.append(e_esp)
    data_esp.append(f_esp) 

    for summary in personal_species:
        para=Para_Clinic_Model.objects.filter(person=summary).last()
        if para.audio_r_tafsir == 'normal':
            a_rg += 1
        elif para.audio_r_tafsir == 'kahesh_shenavai_hedayati':
            b_rg += 1
        elif para.audio_r_tafsir == 'kahesh_shenavai_hesi_asabi':
            c_rg += 1
        elif para.audio_r_tafsir == 'kahesh_shenavai_nashi_az_seda':
            d_rg += 1
        elif para.audio_r_tafsir == 'toaman_hedayati_va_hesi_asabi':
            e_rg += 1
        elif para.audio_r_tafsir == None:
            f_rg += 1
    data_rg.append(a_rg)
    data_rg.append(b_rg)
    data_rg.append(c_rg)
    data_rg.append(d_rg) 
    data_rg.append(e_rg)
    data_rg.append(f_rg) 



    for summary in personal_species:
        para=Para_Clinic_Model.objects.filter(person=summary).last()
        if para.audio_l_tafsir == 'normal':
            a_lg += 1
        elif para.audio_l_tafsir == 'kahesh_shenavai_hedayati':
            b_lg += 1
        elif para.audio_l_tafsir == 'kahesh_shenavai_hesi_asabi':
            c_lg += 1
        elif para.audio_l_tafsir == 'kahesh_shenavai_nashi_az_seda':
            d_lg += 1
        elif para.audio_l_tafsir == 'toaman_hedayati_va_hesi_asabi':
            e_lg += 1
        elif para.audio_l_tafsir == None:
            f_lg += 1
    data_lg.append(a_lg)
    data_lg.append(b_lg)
    data_lg.append(c_lg)
    data_lg.append(d_lg) 
    data_lg.append(e_lg)
    data_lg.append(f_lg) 


    for summary in personal_species:
        experiments=Experiments_Model.objects.filter(person=summary).last()
        if experiments.ua_prot == None or experiments.ua_glu == None or experiments.ua_rbc == None or experiments.ua_wbc == None or experiments.ua_bact == None:
            c_u += 1
        elif experiments.ua_prot_status == False or experiments.ua_glu_status == False or experiments.ua_rbc_status == False or experiments.ua_wbc_status == False or experiments.ua_bact_status == False:
            b_u += 1
        else:
            a_u += 1  
    data_u.append(a_u)
    data_u.append(b_u)
    data_u.append(c_u) 



    for summary in personal_species:
        final=Final_Theory_Model.objects.filter(person=summary).last()
        if final.belamane == True:
            a_p += 1
        elif final.rad == True:
            c_p += 1
        elif final.mashrot == True:
            b_p += 1
        else:
            e_p += 1
    data_p.append(a_p)
    data_p.append(b_p)
    data_p.append(c_p)
    data_p.append(e_p)

    for summary in personal_species:
        experiments=Experiments_Model.objects.filter(person=summary).last()
        if experiments.lead == None:
            d_s += 1  
        elif experiments.lead < 20:
            a_s += 1
        elif experiments.lead < 30:
            b_s += 1
        elif experiments.lead >=30:
            c_s += 1  
    data_s.append(a_s)
    data_s.append(b_s)
    data_s.append(c_s)
    data_s.append(d_s)



    for summary in personal_species:
        experiments=Experiments_Model.objects.filter(person=summary).last()
        if experiments.psa == None:
            c_psa += 1  
        elif experiments.psa_status == True:
            a_psa += 1
        elif experiments.psa_status == False:
            b_psa += 1  
    data_psa.append(a_psa)
    data_psa.append(b_psa)
    data_psa.append(c_psa)


    for summary in personal_species:
        para = Para_Clinic_Model.objects.filter(person=summary).last()
        if para.other_ecg == 'normal':
            a_n += 1
        elif para.other_ecg == 'not_ekhtesasi':
            b_n += 1
        elif para.other_ecg == 'again':
            c_n += 1
        elif para.other_ecg == 'not_normal':
            d_n += 1
        elif  para.other_ecg == None :
            e_n += 1
    data_n.append(a_n)
    data_n.append(b_n)
    data_n.append(c_n)
    data_n.append(d_n)
    data_n.append(e_n)


    for summary in personal_species:
        experiments=Experiments_Model.objects.filter(person=summary).last()
        if experiments.d == None: 
            e_d += 1
        elif experiments.d < 10:
            a_d += 1
        elif experiments.d < 30:
            b_d += 1
        elif experiments.d < 101:
            c_d += 1
        elif experiments.d >= 101:
            d_d += 1
    data_d.append(a_d)
    data_d.append(b_d)
    data_d.append(c_d)
    data_d.append(d_d)
    data_d.append(e_d)



    data=[data_tri,
    data_chl,
    data_sug,
    data_pre,
    data_ry,
    data_ly,
    data_esp,
    data_rg,
    data_lg,
    data_u,
    data_p,
    data_s,
    data_psa,
    data_n,
    data_d]
    context={'personal_species' : personal_species ,'examinations_course':examinations_course,'data':data,'count':count}
    return render(request, 'graph.html',context)


def graph_pdf_view(request):
    options = Options()
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get("http://www.parsianqom.ir/login")
    username = driver.find_element('name',"username")
    password = driver.find_element('name',"password")
    login_but = driver.find_element('name',"login")
    username.send_keys('parsa')
    password.send_keys('690088parsian')
    login_but.click()
    driver.get("http://www.parsianqom.ir/output/graph")
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(1920,S('Height'))
    pdf = FPDF()
    driver.find_element('id','Head').screenshot('images/Head_img.png')
    pdf.add_page()
    pdf.image('images/Head_img.png',-1,None,220,22)
    os.remove('images/Head_img.png')
    pdf.line(0, 31.5, 220, 31.5)
    i = 0
    while i <= 14:        
        if i % 2 == 0 and i != 0:
            driver.find_element('id','graph' + str(i)).screenshot('images/'+ str(i) +'graph_img.png')
            pdf.add_page()
            pdf.image('images/'+ str(i) +'graph_img.png',10,None,200,100)
            os.remove('images/'+ str(i) +'graph_img.png')
            i += 1 
        else:
            driver.find_element('id','graph' + str(i)).screenshot('images/'+ str(i) +'graph_img.png')
            pdf.image('images/'+ str(i) +'graph_img.png',10,None,200,100)
            os.remove('images/'+ str(i) +'graph_img.png')
            i += 1 
    pdf.output("pdfs/graph.pdf", "F")
    file_path = os.path.join('pdfs/graph.pdf')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required(login_url='login')
def solo_output_view(request):
    solo_output_view.current_path = request.get_full_path()
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    job_history=Job_History_Model.objects.all()
    assessment=Assessment_Model.objects.all()
    personal_history=Personal_History_Model.objects.all()
    examinations=Examinations_Model.objects.all()
    experiments=Experiments_Model.objects.all()
    para_clinic=Para_Clinic_Model.objects.all()
    consulting=Consulting_Model.objects.all()
    final_theory=Final_Theory_Model.objects.all()
    count = 0
    for x in personal_species:
        count += 1
    if count % work.order_number == 0:
        count = count // work.order_number
    else:
        count = (count // work.order_number) + 1
    if work:
        number=work.order_number
    else:
        number='1'
    p = Paginator(Personal_Species_Model.objects.filter(examinations_code=examinations_course),number)
    page=request.GET.get('page')
    solo_page=p.get_page(page)
    nums='a' * solo_page.paginator.num_pages
    initial_dict = {
        'order_number':number       
    }
    form=disease_form(initial=initial_dict)
    context={'personal_species' : personal_species,'form' :form,'examinations_course' : examinations_course,'solo_page':solo_page,'nums':nums,'count': count }
    return render(request, 'solo_output.html',context)

def solo_pdf_view(request):
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    options = Options()
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get("http://www.parsianqom.ir/login")
    username = driver.find_element('name',"username")
    password = driver.find_element('name',"password")
    login_but = driver.find_element('name',"login")
    username.send_keys('parsa')
    password.send_keys('690088parsian')
    login_but.click()
    driver.get("http://www.parsianqom.ir"+solo_output_view.current_path)
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(S('Width'),S('Height'))
    i = 0
    count = 0
    pdf = FPDF('P', 'mm', 'A5')
    if personal_species:
        for x in personal_species:
            count += 1
        n = count
        if count < work.order_number:
            last_count = count
        elif count % work.order_number == 0:
            count = count // work.order_number
            last_count = 0
        else:
            count = (count // work.order_number) + 1
            last_count = n - ((count - 1) * work.order_number)
        if n < work.order_number:
            while i < last_count :
                i += 1    
                driver.find_element('id','print' + str(i)).screenshot('images/'+ str(i) +'solo_img.png')
                pdf.add_page()
                pdf.image('images/'+ str(i) +'solo_img.png',0,None,140,140)
                os.remove('images/'+ str(i) +'solo_img.png')
            pdf.output("pdfs/solo.pdf", "F")
            driver.quit()
        elif solo_output_view.current_path == ('/output/solo_output?page=' + str(count)):
            while i < last_count :
                i += 1    
                driver.find_element('id','print' + str(i)).screenshot('images/'+ str(i) +'solo_img.png')
                pdf.add_page()
                pdf.image('images/'+ str(i) +'solo_img.png',0,None,140,140)
                os.remove('images/'+ str(i) +'solo_img.png')
            pdf.output("pdfs/solo.pdf", "F")
            driver.quit()
        else:
            while i < work.order_number :
                i += 1    
                driver.find_element('id','print' + str(i)).screenshot('images/'+ str(i) +'solo_img.png')
                pdf.add_page()
                pdf.image('images/'+ str(i) +'solo_img.png',0,None,140,140)
                os.remove('images/'+ str(i) +'solo_img.png')
            driver.quit()
    else:
        pdf.add_page()
    pdf.output("pdfs/solo.pdf", "F")
    file_path = os.path.join('pdfs/solo.pdf')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required(login_url='login')
def input_view(request):
    return render(request, 'input.html')

@require_POST
def addorder_view(request):
    model=Disease_Model.objects.last()
    form=disease_form(request.POST)
    if form.is_valid():
        model.order_number=form.cleaned_data['order_number']
        model.save()
    return redirect('solo_output')    


@login_required(login_url='login')
def examinations_view(request):
    personal_species=personal_species_form()
    job_history=job_history_form()
    assessment=assessment_form()
    personal_history=personal_history_form()
    examinations=examinations_form()
    experiments=experiments_form()
    para_clinic=para_clinic_form()
    consulting=consulting_form()
    final_theory=final_theory_form()
    context={'personal_species' : personal_species , 'job_history' : job_history , 'assessment' : assessment, 'personal_history' : personal_history, 'examinations' : examinations, 'experiments' : experiments, 'para_clinic' : para_clinic, 'consulting' : consulting , 'final_theory' : final_theory }
    return render(request, 'examinations.html',context)

@require_POST
def addexaminations_view(request):
    username = request.user.username
    e_items=''
    items = ''
    personal_species=personal_species_form(request.POST)
    job_history=job_history_form(request.POST)
    assessment=assessment_form(request.POST)
    personal_history=personal_history_form(request.POST)
    examinations=examinations_form(request.POST)
    experiments=experiments_form(request.POST)
    para_clinic=para_clinic_form(request.POST)
    consulting=consulting_form(request.POST)
    final_theory=final_theory_form(request.POST)
    if personal_species.is_valid():
        new_person = personal_species.save(commit=False)
        new_person.user = username
        if new_person.age:
            new_person.age = 1401 - new_person.age
        if not new_person.fathers_name:
            new_person.fathers_name = 'None'
        if not new_person.personal_code:
            new_person.personal_code = 0
        new_person.save()
    if personal_species.is_valid() and  job_history.is_valid():
        new_job_history = job_history.save(commit=False)
        new_job_history.person = new_person
        if new_job_history.current_job_to_year and new_job_history.current_job_to_month and new_job_history.current_job_from_year and new_job_history.current_job_from_month:
            new_job_history.durations = ((new_job_history.current_job_to_year * 12) + new_job_history.current_job_to_month) - ((new_job_history.current_job_from_year * 12) + new_job_history.current_job_from_month)
        new_job_history.save()
    if personal_species.is_valid() and  assessment.is_valid():
        new_assessment = assessment.save(commit=False)
        new_assessment.person = new_person
        if new_assessment.current_ph_noise == True:
            items += ' سر و صدا/'
        if new_assessment.current_ph_erteash == True:
            items += ' ارتعاش/'
        if new_assessment.current_ph_not_unizan == True:
            items += ' اشعه غیر یونیزان/'
        if new_assessment.current_ph_unizan == True:
            items += ' اشعه یونیزان/'
        if new_assessment.current_ph_stress == True:
            items += ' استرس حرارتی/'
        if new_assessment.current_sh_dust == True:
            items += ' گرد و غبار/'
        if new_assessment.current_sh_metals == True:
            items += ' دمه فلزات/'
        if new_assessment.current_sh_halal == True:
            items += ' حلال/'
        if new_assessment.current_sh_afat == True:
            items += ' آفت کشها/'
        if new_assessment.current_sh_asidvbaz == True:
            items += ' اسید و بازها/'
        if new_assessment.current_sh_gaz == True:
            items += ' گاز ها/'
        if new_assessment.current_bio_gazesh == True:
            items += ' گزش/'
        if new_assessment.current_bio_bactery == True:
            items += ' باکتری/'
        if new_assessment.current_bio_virus == True:
            items += ' ویروس/'
        if new_assessment.current_bio_angal == True:
            items += ' انگل/'
        if new_assessment.current_er_standvsit == True:
            items += ' ایستادن یا نشستن طولانی مدت/'
        if new_assessment.current_er_loop == True:
            items += ' کار تکراری/'
        if new_assessment.current_er_hamlvnaghl == True:
            items += ' حمل و نقل بار سنگین/'
        if new_assessment.current_er_vaziat_namonaseb == True:
            items += ' وضعیت نامناسب بدن/'
        if new_assessment.current_rav_order == True:
            items += ' نوبت کاری/'
        if new_assessment.current_rav_stressor == True:
            items += ' استرسور های شغلی/'  
        if new_assessment.required_description:
            items += new_assessment.required_description
        new_assessment.assessments = items    
        new_assessment.save()
    if personal_species.is_valid() and  personal_history.is_valid():
        new_personal_history = personal_history.save(commit=False)
        new_personal_history.person = new_person
        new_personal_history.save()
    if personal_species.is_valid() and  examinations.is_valid():
        new_examinations = examinations.save(commit=False)
        new_examinations.person = new_person
        if new_examinations.weight and new_examinations.length:
            new_examinations.body_mass=new_examinations.weight / (( new_examinations.length / 100) ** 2 )
        if new_examinations.local_sym_kahesh_vazn == True:
            e_items += "کاهش وزن/"
        if new_examinations.local_sym_kahesh_eshteha == True:
            e_items += "کاهش اشتها/"
        if new_examinations.local_sym_khastegi == True:
            e_items += "خستگی مزمن/"
        if new_examinations.local_sym_ekhtelal_dar_khab == True:
            e_items += "اختلال در خواب/"
        if new_examinations.local_sym_tarigh == True:
            e_items += "تعریق بیش از حد/"
        if new_examinations.local_sym_adam_tahamol == True:
            e_items += "عدم تحمل گرما و سرما/"
        if new_examinations.local_sym_tab == True:
            e_items += "تب/"
        if new_examinations.local_sign_zaheri == True:
            e_items += "وضعیت ظاهری/"
        if new_examinations.local_sign_rang_paride == True:
            e_items += "مخاطات رنگ پریده/"
        if new_examinations.local_des:
            e_items += new_examinations.local_des
            e_items += '/'
        if new_examinations.eye_sym_kahesh_binayi == True:
            e_items += "کاهش حد بینایی/"
        if new_examinations.eye_sym_tari_did == True:
            e_items += "تاری دید/"
        if new_examinations.eye_sym_khastegi == True:
            e_items += "خستگی چشم/"
        if new_examinations.eye_sym_dobini == True:
            e_items += "دوبینی/"
        if new_examinations.eye_sym_sozesh == True:
            e_items += "سوزش چشم/"
        if new_examinations.eye_sym_tars_az_nor == True:
            e_items += "ترس از نور/"
        if new_examinations.eye_sym_ashk == True:
            e_items += "اشک ریزش/"
        if new_examinations.eye_sign_reflex == True:
            e_items += "رفلکس غیر طبیعی مردمک/"
        if new_examinations.eye_sign_red == True:
            e_items += "قرمزی چشم/"
        if new_examinations.eye_sign_sklrai == True:
            e_items += "اسکلرای ایکتریک/"
        if new_examinations.eye_sign_nistagemos == True:
            e_items += "نیستاگموس/"
        if new_examinations.eye_des:
            e_items += new_examinations.eye_des
            e_items += '/'
        if new_examinations.skin_sym_kharesh_post == True:
            e_items += "خارش پوست/"
        if new_examinations.skin_sym_rizesh_mo == True:
            e_items += "ریزش مو/"
        if new_examinations.skin_sym_red == True:
            e_items += "قرمزی پوست/"
        if new_examinations.skin_sym_taghir_post == True:
            e_items += "تغییر رنگ پوست/"
        if new_examinations.skin_sym_zakhm == True:
            e_items += "زخم مزمن/"
        if new_examinations.skin_sym_poste_rizi == True:
            e_items += "پوسته ریزی/"
        if new_examinations.skin_sym_taghir_nakhon == True:
            e_items += "تغییر رنگ ناخن/"
        if new_examinations.skin_sign_makol == True:
            e_items += "ماکول/"
        if new_examinations.skin_sign_papol == True:
            e_items += "پاپول/"
        if new_examinations.skin_sign_nadol == True:
            e_items += "ندول/"
        if new_examinations.skin_sign_vezikol == True:
            e_items += "وزیکول/"
        if new_examinations.skin_sign_zakhm == True:
            e_items += "زخم/"
        if new_examinations.skin_sign_kahir == True:
            e_items += "کهیر/"
        if new_examinations.skin_sign_klabing == True:
            e_items += "کلابینگ/"
        if new_examinations.skin_sign_rizesh_mantaghe == True:
            e_items += "ریزش منطقه ای مو/"
        if new_examinations.skin_sign_rizesh_general == True:
            e_items += "ریزش جنرال مو/"
        if new_examinations.skin_sign_taghirat_peygmani == True:
            e_items += "تغییرات پیگمانی/"
        if new_examinations.skin_des:
            e_items += new_examinations.skin_des
            e_items += "/"
        if new_examinations.gosh_sym_kahesh_shenavaii == True:
            e_items += "کاهش شنوایی/"
        if new_examinations.gosh_sym_vez_vez_gosh == True:
            e_items += "وزوز گوش/"
        if new_examinations.gosh_sym_sargije == True:
            e_items += "سرگیجه واقعی/"
        if new_examinations.gosh_sym_dard_gosh == True:
            e_items += "درد گوش/"
        if new_examinations.gosh_sym_tarashoh_gosh == True:
            e_items += "ترشح گوش/"
        if new_examinations.gosh_sym_gereftegi_seda == True:
            e_items += "گرفتگی صدا/"
        if new_examinations.gosh_sym_galodard == True:
            e_items += "گلودرد/"
        if new_examinations.gosh_sym_abrrizesh_bini == True:
            e_items += "آبریزش بینی/"
        if new_examinations.gosh_sym_ekhtelal_boyayi == True:
            e_items += "اختلال بویایی/"
        if new_examinations.gosh_sym_khareshvsozesh == True:
            e_items += "خارش و سوزش بینی/"
        if new_examinations.gosh_sym_khonrizi == True:
            e_items += "خونریزی بینی/"
        if new_examinations.gosh_sym_khoshki == True:
            e_items += "خشکی دهان/"
        if new_examinations.gosh_sym_ehsas == True:
            e_items += "احساس مزه فلزی در دهان/"
        if new_examinations.gosh_sign_eltehab_parde == True:
            e_items += "التهاب پرده تمپان/"
        if new_examinations.gosh_sign_paregi == True:
            e_items += "پارگی پرده تمپان/"
        if new_examinations.gosh_sign_afzayesh == True:
            e_items += "افزایش غیر طبیعی سرومن/"
        if new_examinations.gosh_sign_tarashoh == True:
            e_items += "ترشح پشت حلق/"
        if new_examinations.gosh_sign_egzodai == True:
            e_items += "اگزودای حلق/"
        if new_examinations.gosh_sign_red == True:
            e_items += "قرمزی حلق/"
        if new_examinations.gosh_sign_polip == True:
            e_items += "پولیپ بینی/"
        if new_examinations.gosh_sign_tndrs == True:
            e_items += "تندرنس سینوس ها/"
        if new_examinations.gosh_sign_lead == True:
            e_items += "lead line/"
        if new_examinations.gosh_sign_bad_smell == True:
            e_items += "بوی بد دهان/"
        if new_examinations.gosh_sign_eltehab_lase == True:
            e_items += "التهاب لثه/"
        if new_examinations.gosh_sign_zakhm == True:
            e_items += "پرفوراسیون/زخم سپتوم/"
        if new_examinations.gosh_des:
            e_items += new_examinations.gosh_des
            e_items += "/"
        if new_examinations.sar_sym_dard_gardan == True:
            e_items += "درد گردن/"
        if new_examinations.sar_sym_tode_gardani == True:
            e_items += "توده گردنی/"
        if new_examinations.sar_sign_bozorgi_tiroid == True:
            e_items += "بزرگی تیروئید/"
        if new_examinations.sar_sign_gardani == True:
            e_items += "لنفادنوپاتی گردنی/"
        if new_examinations.sar_des:
            e_items += new_examinations.sar_des
            e_items += "/"
        if new_examinations.rie_sym_sorfe == True:
            e_items += "سرفه/"
        if new_examinations.rie_sym_khelt == True:
            e_items += "خلط/"
        if new_examinations.rie_sym_tangi == True:
            e_items += "تنگی نفس کوشش/"
        if new_examinations.rie_sym_sine == True:
            e_items += "خس خس سینه/"
        if new_examinations.rie_sign_zaheri == True:
            e_items += "وضعیت ظاهری غیر طبیعی قفسه سینه/"
        if new_examinations.rie_sign_khoshonat == True:
            e_items += "خشونت صدا/"
        if new_examinations.rie_sign_vizing == True:
            e_items += "ویزینگ/"
        if new_examinations.rie_sign_cracel == True:
            e_items += "کراکل/"
        if new_examinations.rie_sign_taki_pene == True:
            e_items += "تاکی پنه/"
        if new_examinations.rie_sign_kahesh_sedaha == True:
            e_items += "کاهش صداهای ریوی/"
        if new_examinations.rie_des:
            e_items += new_examinations.rie_des
            e_items += "/"
        if new_examinations.ghalb_sym_dard == True:
            e_items += "درد قفسه سینه/"
        if new_examinations.ghalb_sym_tapesh == True:
            e_items += "تپش قلب/"
        if new_examinations.ghalb_sym_tangi_shabane == True:
            e_items += "تنگی نفس ناگهانی شبانه/"
        if new_examinations.ghalb_sym_tangi_khabide == True:
            e_items += "تنگی نفس دروضعیت خوابیده/"
        if new_examinations.ghalb_sym_sianoz == True:
            e_items += "سیانوز/"
        if new_examinations.ghalb_sym_senkop == True:
            e_items += "سابقه سنکوپ/"
        if new_examinations.ghalb_sign_s == True:
            e_items += "S1S2غیر طبیعی/"
        if new_examinations.ghalb_sign_seda_ezafe == True:
            e_items += "صدای اضافه قلب/"
        if new_examinations.ghalb_sign_aritmi == True:
            e_items += "آریتمی/"
        if new_examinations.ghalb_sign_varis_tahtani == True:
            e_items += "واریس اندام تحتانی/"
        if new_examinations.ghalb_sign_varis_foghani == True:
            e_items += "واریس اندام فوقانی/"
        if new_examinations.ghalb_sign_andam == True:
            e_items += "ادم اندام/"
        if new_examinations.ghalb_des:
            e_items += new_examinations.ghalb_des
            e_items += "/"
        if new_examinations.shekam_sym_bi_eshteha == True:
            e_items += "بی اشتهایی/"
        if new_examinations.shekam_sym_tahavo == True:
            e_items += "تهوع/"
        if new_examinations.shekam_sym_estefragh == True:
            e_items += "استفراغ/"
        if new_examinations.shekam_sym_dard_shekam == True:
            e_items += "درد شکم/"
        if new_examinations.shekam_sym_soozesh == True:
            e_items += "سوزش سر دل/"
        if new_examinations.shekam_sym_eshal == True:
            e_items += "اسهال/"
        if new_examinations.shekam_sym_yobosat == True:
            e_items += "یبوست/"
        if new_examinations.shekam_sym_ghiri == True:
            e_items += "مدفوع قیری/"
        if new_examinations.shekam_sym_roshan == True:
            e_items += "خون روشن در مدفوع/"
        if new_examinations.shekam_sym_ekhtelal == True:
            e_items += "اختلال در بلع/"
        if new_examinations.shekam_sign_shekami == True:
            e_items += "تندرنس شکمی/"
        if new_examinations.shekam_sign_rebond == True:
            e_items += "ریباند تندرنس/"
        if new_examinations.shekam_sign_hepatomegaly == True:
            e_items += "هپاتومگالی/"
        if new_examinations.shekam_sign_espelnomegali == True:
            e_items += "اسپلنومگالی/"
        if new_examinations.shekam_sign_asib == True:
            e_items += "آسیت/"
        if new_examinations.shekam_sign_tode_shekami == True:
            e_items += "توده شکمی/"
        if new_examinations.shekam_sign_distansion == True:
            e_items += "دیستانسیون شکمی/"
        if new_examinations.shekam_des:
            e_items += new_examinations.shekam_des
            e_items += "/"
        if new_examinations.colie_sym_soozesh == True:
            e_items += "سوزش درار/"
        if new_examinations.colie_sym_tekrar == True:
            e_items += "تکرر ادرار/"
        if new_examinations.colie_sym_khoni == True:
            e_items += "ادرار خونی/"
        if new_examinations.colie_sym_pahlo == True:
            e_items += "درد پهلو/"
        if new_examinations.colie_sym_sangini == True:
            e_items += "احساس سنگینی یا توده در بیضه/"
        if new_examinations.colie_sign_cva == True:
            e_items += "تندرستیCVA/"
        if new_examinations.colie_sign_varikosel == True:
            e_items += "واریکوسل/"
        if new_examinations.colie_des:
            e_items += new_examinations.colie_des
            e_items += "/"
        if new_examinations.eskelety_sym_mafsal == True:
            e_items += "خشکی مفصل/"
        if new_examinations.eskelety_sym_kamar_dard == True:
            e_items += "کمردرد/"
        if new_examinations.eskelety_sym_zano == True:
            e_items += "درد زانو/"
        if new_examinations.eskelety_sym_shane == True:
            e_items += "درد شانه/"
        if new_examinations.eskelety_sym_other_mafasel == True:
            e_items += "درد سایر مفاصل/"
        if new_examinations.eskelety_sign_mahdodiat == True:
            e_items += "محدودیت حرکتی مفصل/"
        if new_examinations.eskelety_sign_kahesh_foghani == True:
            e_items += "کاهش قدرت عضلانی در اندام فوقانی/"
        if new_examinations.eskelety_sign_kahesh_tahtani == True:
            e_items += "کاهش قدرت عضلانی در اندام تحتانی/"
        if new_examinations.eskelety_sign_eskolioz == True:
            e_items += "اسکولیوز/"
        if new_examinations.eskelety_sign_empotasion == True:
            e_items += "امپوتاسیون/"
        if new_examinations.eskelety_sign_slr == True:
            e_items += "تست SLR مثبت/"
        if new_examinations.eskelety_sign_r_slr == True:
            e_items += "تست Reverse-SLR/"
        if new_examinations.eskelety_des:
            e_items += new_examinations.eskelety_des
            e_items += "/"
        if new_examinations.asabi_sym_sar_dard == True:
            e_items += "سردرد/"
        if new_examinations.asabi_sym_giji == True:
            e_items += "گیجی/"
        if new_examinations.asabi_sym_larzesh == True:
            e_items += "لرزش/"
        if new_examinations.asabi_sym_ekhtelal == True:
            e_items += "اختلال حافظه/"
        if new_examinations.asabi_sym_tashanoj == True:
            e_items += "سابقه صرع/تشنج/"
        if new_examinations.asabi_sym_gez_gez == True:
            e_items += "گز گز و مور مور انگشتان دست/"
        if new_examinations.asabi_sign_tabi_e == True:
            e_items += "رفلکس زانوی غیر طبیعی/"
        if new_examinations.asabi_sign_gheir_tabi_e == True:
            e_items += "رفلکس آشیل غیرطبیعی/"
        if new_examinations.asabi_sign_mokhtal == True:
            e_items += "تست رومبرگ مختل/"
        if new_examinations.asabi_sign_trmor == True:
            e_items += "ترمور/"
        if new_examinations.asabi_sign_hesi == True:
            e_items += "اختلال حسی اندام ها/"
        if new_examinations.asabi_sign_tinel == True:
            e_items += "تست تینل مثبت/"
        if new_examinations.asabi_sign_falen == True:
            e_items += "تست فالن مثبت/"
        if new_examinations.asabi_des:
            e_items += new_examinations.asabi_des 
            e_items += "/"
        if new_examinations.ravan_sym_asabaniat == True:
            e_items += "عصبانیت بیش از حد/"
        if new_examinations.ravan_sym_parkhashgari == True:
            e_items += "پرخاشگری/"
        if new_examinations.ravan_sym_ezterab == True:
            e_items += "اضطراب/"
        if new_examinations.ravan_sym_kholgh == True:
            e_items += "خلق پایین/"
        if new_examinations.ravan_sym_angize == True:
            e_items += "کاهش انگیزه/"
        if new_examinations.ravan_sign_hazyan == True:
            e_items += "هذیان/"
        if new_examinations.ravan_sign_tavahom == True:
            e_items += "توهم/"
        if new_examinations.ravan_sign_oriantasion == True:
            e_items += "اختلال اوریانتاسیون/"
        if new_examinations.ravan_des:
            e_items += new_examinations.ravan_des
            e_items += "/" 
        new_examinations.not_normals = e_items    
        new_examinations.save()
    if personal_species.is_valid() and  experiments.is_valid():
        new_experiments = experiments.save(commit=False)
        new_experiments.person = new_person
        if new_experiments.cbc_wbc:
            if new_experiments.cbc_wbc < 3900 or new_experiments.cbc_wbc >11000:
                new_experiments.cbc_wbc_status = False 
            else:
                new_experiments.cbc_wbc_status = True
        else:
            new_experiments.cbc_wbc_status = True
        if new_experiments.cbc_plt:
            if new_experiments.cbc_plt < 140 or new_experiments.cbc_plt >450:
                    new_experiments.cbc_plt_status = False 
            else:
                new_experiments.cbc_plt_status = True
        else:
            new_experiments.cbc_plt_status = True
        if new_experiments.ua_prot:
            if new_experiments.ua_prot < 0 or new_experiments.ua_prot >0:
                    new_experiments.ua_prot_status = False
            else:
                new_experiments.ua_prot_status = True
        else:
            new_experiments.ua_prot_status = True
        if new_experiments.ua_glu:
            if new_experiments.ua_glu < 0 or new_experiments.ua_glu >0:
                    new_experiments.ua_glu_status = False 
            else:
                new_experiments.ua_glu_status = True
        else:
            new_experiments.ua_glu_status = True
        if new_experiments.ua_rbc:
            if new_experiments.ua_rbc > 3:
                new_experiments.ua_rbc_status = False 
            else:
                new_experiments.ua_rbc_status = True
        else:
            new_experiments.ua_rbc_status = True
        if new_experiments.ua_wbc:
            if new_experiments.ua_wbc > 5:
                new_experiments.ua_wbc_status = False 
            else:
                new_experiments.ua_wbc_status = True
        else:
            new_experiments.ua_wbc_status = True
        if new_experiments.ua_bact:
            if new_experiments.ua_bact < 0 or new_experiments.ua_bact > 0:
                new_experiments.ua_bact_status = False 
            else:
                new_experiments.ua_bact_status = True
        else:
            new_experiments.ua_bact_status = True
        if new_experiments.fbs:
            if new_experiments.fbs < 70 or new_experiments.fbs > 125:
                new_experiments.fbs_status = False 
            else:
                new_experiments.fbs_status = True
        else:
            new_experiments.fbs_status = True
        if new_experiments.chol:
            if new_experiments.chol > 200:
                new_experiments.chol_status = False 
            else:
                new_experiments.chol_status = True
        else:
            new_experiments.chol_status = True
        if new_experiments.ldl:
            if new_experiments.ldl > 100:
                new_experiments.ldl_status = False 
            else:
                new_experiments.ldl_status = True
        else:
            new_experiments.ldl_status = True
        if new_experiments.tsh:
            if new_experiments.tsh < 0.4 or new_experiments.tsh > 5:
                new_experiments.tsh_status = False  
            else:
                new_experiments.tsh_status = True
        else:
            new_experiments.tsh_status = True
        if new_experiments.tg:
            if new_experiments.tg > 200:
                new_experiments.tg_status = False 
            else:
                new_experiments.tg_status = True
        else:
            new_experiments.tg_status = True
        if new_experiments.cr:
            if new_experiments.cr >= 1.4:
                new_experiments.cr_status = False 
            else:
                new_experiments.cr_status = True
        else:
            new_experiments.cr_status = True
        if new_experiments.alt:
            if new_experiments.alt >= 40:
                new_experiments.alt_status = False 
            else:
                new_experiments.alt_status = True
        else:
            new_experiments.alt_status = True
        if new_experiments.ast:
            if new_experiments.ast >= 40:
                new_experiments.ast_status = False 
            else:
                new_experiments.ast_status = True
        else:
            new_experiments.ast_status = True
        if new_experiments.ast:
            if new_experiments.alk < 14 or new_experiments.alk > 20:
                    new_experiments.alk_status = False 
            else:
                new_experiments.alk_status = True
        else:
            new_experiments.alk_status = True
        if new_experiments.lead:
            if new_experiments.lead > 20:
                new_experiments.lead_status = False 
            else:
                new_experiments.lead_status = True
        else:
            new_experiments.lead_status = True
        if new_experiments.d:
            if new_experiments.d <= 30 or new_experiments.d >101:
                new_experiments.d_status = False  
            else:
                new_experiments.d_status = True
        else:
            new_experiments.d_status = True
        if new_experiments.psa:
            if new_person.age < 40:
                if new_experiments.psa >= 1.7:
                    new_experiments.psa_status = False
                else:
                    new_experiments.psa_status = True
            if new_person.age < 50 or new_person.age >= 40 :
                if new_experiments.psa >= 2.2:
                    new_experiments.psa_status = False
                else:
                    new_experiments.psa_status = True
            if new_person.age < 60 or new_person.age >= 50:
                if new_experiments.psa >= 3.4:
                    new_experiments.psa_status = False
                else:
                    new_experiments.psa_status = True
            if new_person.age < 70 or new_person.age >= 60:
                if new_experiments.psa >= 6.16:
                    new_experiments.psa_status = False
                else:
                    new_experiments.psa_status = True
            if new_person.age > 70:
                if new_experiments.psa >= 6.77:
                    new_experiments.psa_status = False
                else:
                    new_experiments.psa_status = True
            else:
                new_experiments.psa_status = True
        else:
            new_experiments.psa_status = True
        if new_person.gender == 'mard':
            if new_experiments.cbc_rbc:
                if new_experiments.cbc_rbc < 4 or new_experiments.cbc_rbc >6:
                    new_experiments.cbc_rbc_status = False 
                else:
                    new_experiments.cbc_rbc_status = True
            else:
                new_experiments.cbc_rbc_status = True
            if new_experiments.cbc_hb:
                if new_experiments.cbc_hb < 12 or new_experiments.cbc_hb >16:
                    new_experiments.cbc_hb_status = False 
                else:
                    new_experiments.cbc_hb_status = True
            else:
                new_experiments.cbc_hb_status = True
            if new_experiments.cbc_htc:
                if new_experiments.cbc_htc < 40 or new_experiments.cbc_htc >54:
                    new_experiments.cbc_htc_status = False 
                else:
                    new_experiments.cbc_htc_status = True
            else:
                new_experiments.cbc_htc_status = True
            if new_experiments.hdl:
                if new_experiments.hdl > 40:
                    new_experiments.hdl_status = False    
                else:
                    new_experiments.hdl_status = True 
            else:
                new_experiments.hdl_status = True
        if new_person.gender == 'zan':
            if new_experiments.cbc_rbc:
                if new_experiments.cbc_rbc < 3.5 or new_experiments.cbc_rbc >5:
                    new_experiments.cbc_rbc_status = False 
                else:
                    new_experiments.cbc_rbc_status = True
            else:
                new_experiments.cbc_rbc_status = True
            if new_experiments.cbc_hb:
                if new_experiments.cbc_hb < 11 or new_experiments.cbc_hb >15:
                    new_experiments.cbc_hb_status = False 
                else:
                    new_experiments.cbc_hb_status = True
            else:
                new_experiments.cbc_hb_status = True
            if new_experiments.cbc_htc:
                if new_experiments.cbc_htc < 37 or new_experiments.cbc_htc >47:
                    new_experiments.cbc_htc_status = False 
                else:
                    new_experiments.cbc_htc_status = True
            else:
                new_experiments.cbc_htc_status = True
            if new_experiments.hdl:
                if new_experiments.hdl > 50:
                    new_experiments.hdl_status = False    
                else:
                    new_experiments.hdl_status = True  
            else:
                new_experiments.hdl_status = True    
        new_experiments.save()
    if personal_species.is_valid() and  para_clinic.is_valid():
        new_para_clinic = para_clinic.save(commit=False)
        if new_person.examinations_type == 'badv_estekhdam':
            new_para_clinic.opto_hedat_r_ba = 10
            new_para_clinic.opto_hedat_r_bi = 10
            new_para_clinic.opto_hedat_l_ba = 10
            new_para_clinic.opto_hedat_l_bi = 10
        new_para_clinic.person = new_person
        new_para_clinic.save()
    if personal_species.is_valid() and  consulting.is_valid():
        new_consulting = consulting.save(commit=False)
        new_consulting.person = new_person
        new_consulting.save()
    if personal_species.is_valid() and  final_theory.is_valid():
        new_final_theory = final_theory.save(commit=False)
        new_final_theory.person = new_person
        new_final_theory.save()
    return redirect('examinations')


# @login_required(login_url='login')
# def examinations_output_course_view(request):
#     form=disease_form()
#     model=Disease_Model.objects.last()
#     if model:
#         code=model.examinations_code
#     else:
#         code=''
#     examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
#     personal_species=Personal_Species_Model.objects.filter(name=model.name,age=1401 - model.age,fathers_name=model.fathers_name,personal_code=model.personal_code,examinations_code=examinations_course).last()
#     job_history=Job_History_Model.objects.filter(person=personal_species).last()
#     assessment=Assessment_Model.objects.filter(person=personal_species).last()
#     personal_history=Personal_History_Model.objects.filter(person=personal_species).last()
#     examinations=Examinations_Model.objects.filter(person=personal_species).last()
#     experiments=Experiments_Model.objects.filter(person=personal_species).last()
#     para_clinic=Para_Clinic_Model.objects.filter(person=personal_species).last()
#     consulting=Consulting_Model.objects.filter(person=personal_species).last()
#     final_theory=Final_Theory_Model.objects.filter(person=personal_species).last()
#     context={'form':form, 'personal_species' : personal_species , 'job_history' : job_history , 'assessment' : assessment, 'personal_history' : personal_history, 'examinations' : examinations, 'experiments' : experiments, 'para_clinic' : para_clinic, 'consulting' : consulting , 'final_theory' : final_theory }
#     return render(request, 'examinations_output_course.html',context)


@login_required(login_url='login')
def examinations_output_course_view(request):
    form=disease_form()
    model=Disease_Model.objects.last()
    if model:
        code=model.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    job_history=Job_History_Model.objects.filter(person=personal_species)
    assessment=Assessment_Model.objects.filter(person=personal_species)
    personal_history=Personal_History_Model.objects.filter(person=personal_species)
    examinations=Examinations_Model.objects.filter(person=personal_species)
    experiments=Experiments_Model.objects.filter(person=personal_species)
    para_clinic=Para_Clinic_Model.objects.filter(person=personal_species)
    consulting=Consulting_Model.objects.filter(person=personal_species)
    final_theory=Final_Theory_Model.objects.filter(person=personal_species)
    context={'form':form, 'personal_species' : personal_species , 'job_history' : job_history , 'assessment' : assessment, 'personal_history' : personal_history, 'examinations' : examinations, 'experiments' : experiments, 'para_clinic' : para_clinic, 'consulting' : consulting , 'final_theory' : final_theory }
    return render(request, 'examinations_output_course.html',context)


def examinations_output_course_pdf_view(request):
    work=Disease_Model.objects.last()
    if work:
        code=work.examinations_code
    else:
        code=''
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    personal_species=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("http://www.parsianqom.ir/login")
    username = driver.find_element('name',"username")
    password = driver.find_element('name',"password")
    login_but = driver.find_element('name',"login")
    username.send_keys('parsa')
    password.send_keys('690088parsian')
    login_but.click()
    driver.get("http://www.parsianqom.ir/output/examinations_output/course")
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(1920,S('Height'))
    count = 0
    i = 0
    pdf = FPDF()
    for a in personal_species:
        i = int(i)
        i += 1
        i = str(i)
        WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located((By.ID, "examinations0"))).screenshot('images/examinations0' + i +'.png')
        pdf.add_page()
        pdf.image('images/examinations0' + i +'.png',4,None,200,240)
        os.remove('images/examinations0' + i +'.png')
        WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located((By.ID, "examinations1"))).screenshot('images/examinations1' + i +'.png')
        pdf.add_page()
        pdf.image('images/examinations1' + i +'.png',4,None,200,180)
        os.remove('images/examinations1' + i +'.png')
        WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located((By.ID, "examinations2"))).screenshot('images/examinations2' + i +'.png')
        pdf.add_page()
        pdf.image('images/examinations2' + i +'.png',10,None,180,265)
        os.remove('images/examinations2' + i +'.png')
        WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located((By.ID, "examinations3"))).screenshot('images/examinations3' + i +'.png')
        pdf.add_page()
        pdf.image('images/examinations3' + i +'.png',4,None,200,265)
        os.remove('images/examinations3' + i +'.png')
        WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located((By.ID, "examinations4"))).screenshot('images/examinations4' + i +'.png')
        pdf.add_page()
        pdf.image('images/examinations4' + i +'.png',4,None,200,140)
        os.remove('images/examinations4' + i +'.png')
    pdf.output("pdfs/examinations_course.pdf", "F")
    file_path = os.path.join('pdfs/examinations_course.pdf')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required(login_url='login')
def examinations_output_person_view(request):
    form=disease_form()
    model=Disease_Model.objects.last()
    if model:
        code=model.p_examinations_code
    else:
        code=''
    if model.p_age:
        code_list=Personal_Species_Model.objects.filter(name=model.p_name,age=1401 - model.p_age,fathers_name=model.p_fathers_name,personal_code=model.p_personal_code)
    else:
        code_list=[]
    if model.p_examinations_code != 'all' and model.p_examinations_code:
        examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
        personal_species=Personal_Species_Model.objects.filter(name=model.p_name,age=1401 - model.p_age,fathers_name=model.p_fathers_name,personal_code=model.p_personal_code,examinations_code=examinations_course)
    elif model.p_age and model.p_examinations_code == 'all':
        personal_species=Personal_Species_Model.objects.filter(name=model.p_name,age=1401 - model.p_age,fathers_name=model.p_fathers_name,personal_code=model.p_personal_code)
    else:
        personal_species = []
    examination_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    inputlist=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    context={'form':form, 'personal_species' : personal_species , 'code_list' : code_list ,'inputlist' : inputlist}
    return render(request, 'examinations_output_person.html',context)


def examinations_output_person_pdf_view(request):
    model=Disease_Model.objects.last()
    if model:
        code=model.p_examinations_code
    else:
        code=''
    if model.p_examinations_code != 'all' and model.p_examinations_code:
        examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
        personal_species=Personal_Species_Model.objects.filter(name=model.p_name,age=1401 - model.p_age,fathers_name=model.p_fathers_name,personal_code=model.p_personal_code,examinations_code=examinations_course)
    elif model.p_age and model.p_examinations_code == 'all':
        personal_species=Personal_Species_Model.objects.filter(name=model.p_name,age=1401 - model.p_age,fathers_name=model.p_fathers_name,personal_code=model.p_personal_code)
    else:
        personal_species = []
    options = Options()
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get("http://www.parsianqom.ir/login")
    username = driver.find_element('name',"username")
    password = driver.find_element('name',"password")
    login_but = driver.find_element('name',"login")
    username.send_keys('parsa')
    password.send_keys('690088parsian')
    login_but.click()
    driver.get("http://www.parsianqom.ir/output/examinations_output/person")
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(1920,S('Height'))
    count = 0
    i = 0
    pdf = FPDF()
    for a in personal_species:
        i = int(i)
        i += 1
        i = str(i)
        driver.find_element('id','examinations0' + i).screenshot('images/examinations0' + i +'.png')
        pdf.add_page()
        pdf.image('images/examinations0' + i +'.png',4,None,200,240)
        os.remove('images/examinations0' + i +'.png')
        driver.find_element('id','examinations1' + i).screenshot('images/examinations1' + i +'.png')
        pdf.add_page()
        pdf.image('images/examinations1' + i +'.png',4,None,200,180)
        os.remove('images/examinations1' + i +'.png')
        driver.find_element('id','examinations2' + i).screenshot('images/examinations2' + i +'.png')
        pdf.add_page()
        pdf.image('images/examinations2' + i +'.png',10,None,180,265)
        os.remove('images/examinations2' + i +'.png')
        driver.find_element('id','examinations3' + i).screenshot('images/examinations3' + i +'.png')
        pdf.add_page()
        pdf.image('images/examinations3' + i +'.png',4,None,200,265)
        os.remove('images/examinations3' + i +'.png')
        driver.find_element('id','examinations4' + i).screenshot('images/examinations4' + i +'.png')
        pdf.add_page()
        pdf.image('images/examinations4' + i +'.png',4,None,200,140)
        os.remove('images/examinations4' + i +'.png')
    pdf.output("pdfs/examinations.pdf", "F")
    file_path = os.path.join('pdfs/examinations.pdf')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@require_POST
def addexaminations_output_view(request):
    model=Disease_Model.objects.last()
    form=disease_form(request.POST)
    if form.is_valid():
        model.name=form.cleaned_data['name']
        model.fathers_name=form.cleaned_data['fathers_name']
        model.age=form.cleaned_data['age']
        model.personal_code=form.cleaned_data['personal_code']
        model.save()
    return redirect('examinations_output')


def examinations_output_edit_view(request):
    form=disease_form()
    username = request.user.username
    code_list=ExaminationsCourse.objects.order_by('id')
    e_items=''
    items = ''
    
    model=Disease_Model.objects.last()
    if model:
        code=model.p_examinations_code
    else:
        code=''
        
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=model.examinations_code).last()
    personal_species_m=Personal_Species_Model.objects.filter(name=model.e_name,age=1401 - model.e_age,fathers_name=model.e_fathers_name,personal_code=model.e_personal_code,examinations_code=examinations_course).last()
    job_history_m=Job_History_Model.objects.filter(person=personal_species_m).last()
    assessment_m=Assessment_Model.objects.filter(person=personal_species_m).last()
    personal_history_m=Personal_History_Model.objects.filter(person=personal_species_m).last()
    examinations_m=Examinations_Model.objects.filter(person=personal_species_m).last()
    experiments_m=Experiments_Model.objects.filter(person=personal_species_m).last()
    para_clinic_m=Para_Clinic_Model.objects.filter(person=personal_species_m).last()
    consulting_m=Consulting_Model.objects.filter(person=personal_species_m).last()
    final_theory_m=Final_Theory_Model.objects.filter(person=personal_species_m).last()
    personal_species=personal_species_form(request.POST or None,instance=personal_species_m)
    job_history=job_history_form(request.POST or None,instance=job_history_m)
    assessment=assessment_form(request.POST or None,instance=assessment_m)
    personal_history=personal_history_form(request.POST or None,instance=personal_history_m)
    examinations=examinations_form(request.POST or None,instance=examinations_m)
    experiments=experiments_form(request.POST or None,instance=experiments_m)
    para_clinic=para_clinic_form(request.POST or None,instance=para_clinic_m)
    consulting=consulting_form(request.POST or None,instance=consulting_m)
    final_theory=final_theory_form(request.POST or None,instance=final_theory_m)

    if personal_species.is_valid():
        new_person = personal_species.save(commit=False)
        new_person.user = username
        if not new_person.fathers_name:
            new_person.fathers_name = 'None'
        if not new_person.personal_code:
            new_person.personal_code = 0
        new_person.save()
    if personal_species.is_valid() and  job_history.is_valid():
        new_job_history = job_history.save(commit=False)
        new_job_history.person = new_person
        if new_job_history.current_job_to_year and new_job_history.current_job_to_month and new_job_history.current_job_from_year and new_job_history.current_job_from_month:
            new_job_history.durations = ((new_job_history.current_job_to_year * 12) + new_job_history.current_job_to_month) - ((new_job_history.current_job_from_year * 12) + new_job_history.current_job_from_month)
        new_job_history.save()
    if personal_species.is_valid() and  assessment.is_valid():
        new_assessment = assessment.save(commit=False)
        new_assessment.person = new_person
        if new_assessment.current_ph_noise == True:
            items += ' سر و صدا/'
        if new_assessment.current_ph_erteash == True:
            items += ' ارتعاش/'
        if new_assessment.current_ph_not_unizan == True:
            items += ' اشعه غیر یونیزان/'
        if new_assessment.current_ph_unizan == True:
            items += ' اشعه یونیزان/'
        if new_assessment.current_ph_stress == True:
            items += ' استرس حرارتی/'
        if new_assessment.current_sh_dust == True:
            items += ' گرد و غبار/'
        if new_assessment.current_sh_metals == True:
            items += ' دمه فلزات/'
        if new_assessment.current_sh_halal == True:
            items += ' حلال/'
        if new_assessment.current_sh_afat == True:
            items += ' آفت کشها/'
        if new_assessment.current_sh_asidvbaz == True:
            items += ' اسید و بازها/'
        if new_assessment.current_sh_gaz == True:
            items += ' گاز ها/'
        if new_assessment.current_bio_gazesh == True:
            items += ' گزش/'
        if new_assessment.current_bio_bactery == True:
            items += ' باکتری/'
        if new_assessment.current_bio_virus == True:
            items += ' ویروس/'
        if new_assessment.current_bio_angal == True:
            items += ' انگل/'
        if new_assessment.current_er_standvsit == True:
            items += ' ایستادن یا نشستن طولانی مدت/'
        if new_assessment.current_er_loop == True:
            items += ' کار تکراری/'
        if new_assessment.current_er_hamlvnaghl == True:
            items += ' حمل و نقل بار سنگین/'
        if new_assessment.current_er_vaziat_namonaseb == True:
            items += ' وضعیت نامناسب بدن/'
        if new_assessment.current_rav_order == True:
            items += ' نوبت کاری/'
        if new_assessment.current_rav_stressor == True:
            items += ' استرسور های شغلی/'  
        if new_assessment.required_description:
            items += new_assessment.required_description
        new_assessment.assessments = items    
        new_assessment.save()
    if personal_species.is_valid() and  personal_history.is_valid():
        new_personal_history = personal_history.save(commit=False)
        new_personal_history.person = new_person
        new_personal_history.save()
    if personal_species.is_valid() and  examinations.is_valid():
        new_examinations = examinations.save(commit=False)
        new_examinations.person = new_person
        if new_examinations.weight and new_examinations.length:
            new_examinations.body_mass=new_examinations.weight / (( new_examinations.length / 100) ** 2 )
        if new_examinations.local_sym_kahesh_vazn == True:
            e_items += "کاهش وزن/"
        if new_examinations.local_sym_kahesh_eshteha == True:
            e_items += "کاهش اشتها/"
        if new_examinations.local_sym_khastegi == True:
            e_items += "خستگی مزمن/"
        if new_examinations.local_sym_ekhtelal_dar_khab == True:
            e_items += "اختلال در خواب/"
        if new_examinations.local_sym_tarigh == True:
            e_items += "تعریق بیش از حد/"
        if new_examinations.local_sym_adam_tahamol == True:
            e_items += "عدم تحمل گرما و سرما/"
        if new_examinations.local_sym_tab == True:
            e_items += "تب/"
        if new_examinations.local_sign_zaheri == True:
            e_items += "وضعیت ظاهری/"
        if new_examinations.local_sign_rang_paride == True:
            e_items += "مخاطات رنگ پریده/"
        if new_examinations.local_des:
            e_items += new_examinations.local_des
            e_items += '/'
        if new_examinations.eye_sym_kahesh_binayi == True:
            e_items += "کاهش حد بینایی/"
        if new_examinations.eye_sym_tari_did == True:
            e_items += "تاری دید/"
        if new_examinations.eye_sym_khastegi == True:
            e_items += "خستگی چشم/"
        if new_examinations.eye_sym_dobini == True:
            e_items += "دوبینی/"
        if new_examinations.eye_sym_sozesh == True:
            e_items += "سوزش چشم/"
        if new_examinations.eye_sym_tars_az_nor == True:
            e_items += "ترس از نور/"
        if new_examinations.eye_sym_ashk == True:
            e_items += "اشک ریزش/"
        if new_examinations.eye_sign_reflex == True:
            e_items += "رفلکس غیر طبیعی مردمک/"
        if new_examinations.eye_sign_red == True:
            e_items += "قرمزی چشم/"
        if new_examinations.eye_sign_sklrai == True:
            e_items += "اسکلرای ایکتریک/"
        if new_examinations.eye_sign_nistagemos == True:
            e_items += "نیستاگموس/"
        if new_examinations.eye_des:
            e_items += new_examinations.eye_des
            e_items += '/'
        if new_examinations.skin_sym_kharesh_post == True:
            e_items += "خارش پوست/"
        if new_examinations.skin_sym_rizesh_mo == True:
            e_items += "ریزش مو/"
        if new_examinations.skin_sym_red == True:
            e_items += "قرمزی پوست/"
        if new_examinations.skin_sym_taghir_post == True:
            e_items += "تغییر رنگ پوست/"
        if new_examinations.skin_sym_zakhm == True:
            e_items += "زخم مزمن/"
        if new_examinations.skin_sym_poste_rizi == True:
            e_items += "پوسته ریزی/"
        if new_examinations.skin_sym_taghir_nakhon == True:
            e_items += "تغییر رنگ ناخن/"
        if new_examinations.skin_sign_makol == True:
            e_items += "ماکول/"
        if new_examinations.skin_sign_papol == True:
            e_items += "پاپول/"
        if new_examinations.skin_sign_nadol == True:
            e_items += "ندول/"
        if new_examinations.skin_sign_vezikol == True:
            e_items += "وزیکول/"
        if new_examinations.skin_sign_zakhm == True:
            e_items += "زخم/"
        if new_examinations.skin_sign_kahir == True:
            e_items += "کهیر/"
        if new_examinations.skin_sign_klabing == True:
            e_items += "کلابینگ/"
        if new_examinations.skin_sign_rizesh_mantaghe == True:
            e_items += "ریزش منطقه ای مو/"
        if new_examinations.skin_sign_rizesh_general == True:
            e_items += "ریزش جنرال مو/"
        if new_examinations.skin_sign_taghirat_peygmani == True:
            e_items += "تغییرات پیگمانی/"
        if new_examinations.skin_des:
            e_items += new_examinations.skin_des
            e_items += "/"
        if new_examinations.gosh_sym_kahesh_shenavaii == True:
            e_items += "کاهش شنوایی/"
        if new_examinations.gosh_sym_vez_vez_gosh == True:
            e_items += "وزوز گوش/"
        if new_examinations.gosh_sym_sargije == True:
            e_items += "سرگیجه واقعی/"
        if new_examinations.gosh_sym_dard_gosh == True:
            e_items += "درد گوش/"
        if new_examinations.gosh_sym_tarashoh_gosh == True:
            e_items += "ترشح گوش/"
        if new_examinations.gosh_sym_gereftegi_seda == True:
            e_items += "گرفتگی صدا/"
        if new_examinations.gosh_sym_galodard == True:
            e_items += "گلودرد/"
        if new_examinations.gosh_sym_abrrizesh_bini == True:
            e_items += "آبریزش بینی/"
        if new_examinations.gosh_sym_ekhtelal_boyayi == True:
            e_items += "اختلال بویایی/"
        if new_examinations.gosh_sym_khareshvsozesh == True:
            e_items += "خارش و سوزش بینی/"
        if new_examinations.gosh_sym_khonrizi == True:
            e_items += "خونریزی بینی/"
        if new_examinations.gosh_sym_khoshki == True:
            e_items += "خشکی دهان/"
        if new_examinations.gosh_sym_ehsas == True:
            e_items += "احساس مزه فلزی در دهان/"
        if new_examinations.gosh_sign_eltehab_parde == True:
            e_items += "التهاب پرده تمپان/"
        if new_examinations.gosh_sign_paregi == True:
            e_items += "پارگی پرده تمپان/"
        if new_examinations.gosh_sign_afzayesh == True:
            e_items += "افزایش غیر طبیعی سرومن/"
        if new_examinations.gosh_sign_tarashoh == True:
            e_items += "ترشح پشت حلق/"
        if new_examinations.gosh_sign_egzodai == True:
            e_items += "اگزودای حلق/"
        if new_examinations.gosh_sign_red == True:
            e_items += "قرمزی حلق/"
        if new_examinations.gosh_sign_polip == True:
            e_items += "پولیپ بینی/"
        if new_examinations.gosh_sign_tndrs == True:
            e_items += "تندرنس سینوس ها/"
        if new_examinations.gosh_sign_lead == True:
            e_items += "lead line/"
        if new_examinations.gosh_sign_bad_smell == True:
            e_items += "بوی بد دهان/"
        if new_examinations.gosh_sign_eltehab_lase == True:
            e_items += "التهاب لثه/"
        if new_examinations.gosh_sign_zakhm == True:
            e_items += "پرفوراسیون/زخم سپتوم/"
        if new_examinations.gosh_des:
            e_items += new_examinations.gosh_des
            e_items += "/"
        if new_examinations.sar_sym_dard_gardan == True:
            e_items += "درد گردن/"
        if new_examinations.sar_sym_tode_gardani == True:
            e_items += "توده گردنی/"
        if new_examinations.sar_sign_bozorgi_tiroid == True:
            e_items += "بزرگی تیروئید/"
        if new_examinations.sar_sign_gardani == True:
            e_items += "لنفادنوپاتی گردنی/"
        if new_examinations.sar_des:
            e_items += new_examinations.sar_des
            e_items += "/"
        if new_examinations.rie_sym_sorfe == True:
            e_items += "سرفه/"
        if new_examinations.rie_sym_khelt == True:
            e_items += "خلط/"
        if new_examinations.rie_sym_tangi == True:
            e_items += "تنگی نفس کوشش/"
        if new_examinations.rie_sym_sine == True:
            e_items += "خس خس سینه/"
        if new_examinations.rie_sign_zaheri == True:
            e_items += "وضعیت ظاهری غیر طبیعی قفسه سینه/"
        if new_examinations.rie_sign_khoshonat == True:
            e_items += "خشونت صدا/"
        if new_examinations.rie_sign_vizing == True:
            e_items += "ویزینگ/"
        if new_examinations.rie_sign_cracel == True:
            e_items += "کراکل/"
        if new_examinations.rie_sign_taki_pene == True:
            e_items += "تاکی پنه/"
        if new_examinations.rie_sign_kahesh_sedaha == True:
            e_items += "کاهش صداهای ریوی/"
        if new_examinations.rie_des:
            e_items += new_examinations.rie_des
            e_items += "/"
        if new_examinations.ghalb_sym_dard == True:
            e_items += "درد قفسه سینه/"
        if new_examinations.ghalb_sym_tapesh == True:
            e_items += "تپش قلب/"
        if new_examinations.ghalb_sym_tangi_shabane == True:
            e_items += "تنگی نفس ناگهانی شبانه/"
        if new_examinations.ghalb_sym_tangi_khabide == True:
            e_items += "تنگی نفس دروضعیت خوابیده/"
        if new_examinations.ghalb_sym_sianoz == True:
            e_items += "سیانوز/"
        if new_examinations.ghalb_sym_senkop == True:
            e_items += "سابقه سنکوپ/"
        if new_examinations.ghalb_sign_s == True:
            e_items += "S1S2غیر طبیعی/"
        if new_examinations.ghalb_sign_seda_ezafe == True:
            e_items += "صدای اضافه قلب/"
        if new_examinations.ghalb_sign_aritmi == True:
            e_items += "آریتمی/"
        if new_examinations.ghalb_sign_varis_tahtani == True:
            e_items += "واریس اندام تحتانی/"
        if new_examinations.ghalb_sign_varis_foghani == True:
            e_items += "واریس اندام فوقانی/"
        if new_examinations.ghalb_sign_andam == True:
            e_items += "ادم اندام/"
        if new_examinations.ghalb_des:
            e_items += new_examinations.ghalb_des
            e_items += "/"
        if new_examinations.shekam_sym_bi_eshteha == True:
            e_items += "بی اشتهایی/"
        if new_examinations.shekam_sym_tahavo == True:
            e_items += "تهوع/"
        if new_examinations.shekam_sym_estefragh == True:
            e_items += "استفراغ/"
        if new_examinations.shekam_sym_dard_shekam == True:
            e_items += "درد شکم/"
        if new_examinations.shekam_sym_soozesh == True:
            e_items += "سوزش سر دل/"
        if new_examinations.shekam_sym_eshal == True:
            e_items += "اسهال/"
        if new_examinations.shekam_sym_yobosat == True:
            e_items += "یبوست/"
        if new_examinations.shekam_sym_ghiri == True:
            e_items += "مدفوع قیری/"
        if new_examinations.shekam_sym_roshan == True:
            e_items += "خون روشن در مدفوع/"
        if new_examinations.shekam_sym_ekhtelal == True:
            e_items += "اختلال در بلع/"
        if new_examinations.shekam_sign_shekami == True:
            e_items += "تندرنس شکمی/"
        if new_examinations.shekam_sign_rebond == True:
            e_items += "ریباند تندرنس/"
        if new_examinations.shekam_sign_hepatomegaly == True:
            e_items += "هپاتومگالی/"
        if new_examinations.shekam_sign_espelnomegali == True:
            e_items += "اسپلنومگالی/"
        if new_examinations.shekam_sign_asib == True:
            e_items += "آسیت/"
        if new_examinations.shekam_sign_tode_shekami == True:
            e_items += "توده شکمی/"
        if new_examinations.shekam_sign_distansion == True:
            e_items += "دیستانسیون شکمی/"
        if new_examinations.shekam_des:
            e_items += new_examinations.shekam_des
            e_items += "/"
        if new_examinations.colie_sym_soozesh == True:
            e_items += "سوزش درار/"
        if new_examinations.colie_sym_tekrar == True:
            e_items += "تکرر ادرار/"
        if new_examinations.colie_sym_khoni == True:
            e_items += "ادرار خونی/"
        if new_examinations.colie_sym_pahlo == True:
            e_items += "درد پهلو/"
        if new_examinations.colie_sym_sangini == True:
            e_items += "احساس سنگینی یا توده در بیضه/"
        if new_examinations.colie_sign_cva == True:
            e_items += "تندرستیCVA/"
        if new_examinations.colie_sign_varikosel == True:
            e_items += "واریکوسل/"
        if new_examinations.colie_des:
            e_items += new_examinations.colie_des
            e_items += "/"
        if new_examinations.eskelety_sym_mafsal == True:
            e_items += "خشکی مفصل/"
        if new_examinations.eskelety_sym_kamar_dard == True:
            e_items += "کمردرد/"
        if new_examinations.eskelety_sym_zano == True:
            e_items += "درد زانو/"
        if new_examinations.eskelety_sym_shane == True:
            e_items += "درد شانه/"
        if new_examinations.eskelety_sym_other_mafasel == True:
            e_items += "درد سایر مفاصل/"
        if new_examinations.eskelety_sign_mahdodiat == True:
            e_items += "محدودیت حرکتی مفصل/"
        if new_examinations.eskelety_sign_kahesh_foghani == True:
            e_items += "کاهش قدرت عضلانی در اندام فوقانی/"
        if new_examinations.eskelety_sign_kahesh_tahtani == True:
            e_items += "کاهش قدرت عضلانی در اندام تحتانی/"
        if new_examinations.eskelety_sign_eskolioz == True:
            e_items += "اسکولیوز/"
        if new_examinations.eskelety_sign_empotasion == True:
            e_items += "امپوتاسیون/"
        if new_examinations.eskelety_sign_slr == True:
            e_items += "تست SLR مثبت/"
        if new_examinations.eskelety_sign_r_slr == True:
            e_items += "تست Reverse-SLR/"
        if new_examinations.eskelety_des:
            e_items += new_examinations.eskelety_des
            e_items += "/"
        if new_examinations.asabi_sym_sar_dard == True:
            e_items += "سردرد/"
        if new_examinations.asabi_sym_giji == True:
            e_items += "گیجی/"
        if new_examinations.asabi_sym_larzesh == True:
            e_items += "لرزش/"
        if new_examinations.asabi_sym_ekhtelal == True:
            e_items += "اختلال حافظه/"
        if new_examinations.asabi_sym_tashanoj == True:
            e_items += "سابقه صرع/تشنج/"
        if new_examinations.asabi_sym_gez_gez == True:
            e_items += "گز گز و مور مور انگشتان دست/"
        if new_examinations.asabi_sign_tabi_e == True:
            e_items += "رفلکس زانوی غیر طبیعی/"
        if new_examinations.asabi_sign_gheir_tabi_e == True:
            e_items += "رفلکس آشیل غیرطبیعی/"
        if new_examinations.asabi_sign_mokhtal == True:
            e_items += "تست رومبرگ مختل/"
        if new_examinations.asabi_sign_trmor == True:
            e_items += "ترمور/"
        if new_examinations.asabi_sign_hesi == True:
            e_items += "اختلال حسی اندام ها/"
        if new_examinations.asabi_sign_tinel == True:
            e_items += "تست تینل مثبت/"
        if new_examinations.asabi_sign_falen == True:
            e_items += "تست فالن مثبت/"
        if new_examinations.asabi_des:
            e_items += new_examinations.asabi_des 
            e_items += "/"
        if new_examinations.ravan_sym_asabaniat == True:
            e_items += "عصبانیت بیش از حد/"
        if new_examinations.ravan_sym_parkhashgari == True:
            e_items += "پرخاشگری/"
        if new_examinations.ravan_sym_ezterab == True:
            e_items += "اضطراب/"
        if new_examinations.ravan_sym_kholgh == True:
            e_items += "خلق پایین/"
        if new_examinations.ravan_sym_angize == True:
            e_items += "کاهش انگیزه/"
        if new_examinations.ravan_sign_hazyan == True:
            e_items += "هذیان/"
        if new_examinations.ravan_sign_tavahom == True:
            e_items += "توهم/"
        if new_examinations.ravan_sign_oriantasion == True:
            e_items += "اختلال اوریانتاسیون/"
        if new_examinations.ravan_des:
            e_items += new_examinations.ravan_des
            e_items += "/" 
        new_examinations.not_normals = e_items    
        new_examinations.save()
    if personal_species.is_valid() and  experiments.is_valid():
        new_experiments = experiments.save(commit=False)
        new_experiments.person = new_person
        if new_experiments.cbc_wbc:
            if new_experiments.cbc_wbc < 3900 or new_experiments.cbc_wbc >11000:
                new_experiments.cbc_wbc_status = False 
            else:
                new_experiments.cbc_wbc_status = True
        else:
            new_experiments.cbc_wbc_status = True
        if new_experiments.cbc_plt:
            if new_experiments.cbc_plt < 140 or new_experiments.cbc_plt >450:
                    new_experiments.cbc_plt_status = False 
            else:
                new_experiments.cbc_plt_status = True
        else:
            new_experiments.cbc_plt_status = True
        if new_experiments.ua_prot:
            if new_experiments.ua_prot < 0 or new_experiments.ua_prot >0:
                    new_experiments.ua_prot_status = False
            else:
                new_experiments.ua_prot_status = True
        else:
            new_experiments.ua_prot_status = True
        if new_experiments.ua_glu:
            if new_experiments.ua_glu < 0 or new_experiments.ua_glu >0:
                    new_experiments.ua_glu_status = False 
            else:
                new_experiments.ua_glu_status = True
        else:
            new_experiments.ua_glu_status = True
        if new_experiments.ua_rbc:
            if new_experiments.ua_rbc > 3:
                new_experiments.ua_rbc_status = False 
            else:
                new_experiments.ua_rbc_status = True
        else:
            new_experiments.ua_rbc_status = True
        if new_experiments.ua_wbc:
            if new_experiments.ua_wbc > 5:
                new_experiments.ua_wbc_status = False 
            else:
                new_experiments.ua_wbc_status = True
        else:
            new_experiments.ua_wbc_status = True
        if new_experiments.ua_bact:
            if new_experiments.ua_bact < 0 or new_experiments.ua_bact > 0:
                new_experiments.ua_bact_status = False 
            else:
                new_experiments.ua_bact_status = True
        else:
            new_experiments.ua_bact_status = True
        if new_experiments.fbs:
            if new_experiments.fbs < 70 or new_experiments.fbs > 125:
                new_experiments.fbs_status = False 
            else:
                new_experiments.fbs_status = True
        else:
            new_experiments.fbs_status = True
        if new_experiments.chol:
            if new_experiments.chol > 200:
                new_experiments.chol_status = False 
            else:
                new_experiments.chol_status = True
        else:
            new_experiments.chol_status = True
        if new_experiments.ldl:
            if new_experiments.ldl > 100:
                new_experiments.ldl_status = False 
            else:
                new_experiments.ldl_status = True
        else:
            new_experiments.ldl_status = True
        if new_experiments.tsh:
            if new_experiments.tsh < 0.4 or new_experiments.tsh > 5:
                new_experiments.tsh_status = False  
            else:
                new_experiments.tsh_status = True
        else:
            new_experiments.tsh_status = True
        if new_experiments.tg:
            if new_experiments.tg > 200:
                new_experiments.tg_status = False 
            else:
                new_experiments.tg_status = True
        else:
            new_experiments.tg_status = True
        if new_experiments.cr:
            if new_experiments.cr >= 1.4:
                new_experiments.cr_status = False 
            else:
                new_experiments.cr_status = True
        else:
            new_experiments.cr_status = True
        if new_experiments.alt:
            if new_experiments.alt >= 40:
                new_experiments.alt_status = False 
            else:
                new_experiments.alt_status = True
        else:
            new_experiments.alt_status = True
        if new_experiments.ast:
            if new_experiments.ast >= 40:
                new_experiments.ast_status = False 
            else:
                new_experiments.ast_status = True
        else:
            new_experiments.ast_status = True
        if new_experiments.ast:
            if new_experiments.alk < 14 or new_experiments.alk > 20:
                    new_experiments.alk_status = False 
            else:
                new_experiments.alk_status = True
        else:
            new_experiments.alk_status = True
        if new_experiments.lead:
            if new_experiments.lead > 20:
                new_experiments.lead_status = False 
            else:
                new_experiments.lead_status = True
        else:
            new_experiments.lead_status = True
        if new_experiments.d:
            if new_experiments.d <= 30 or new_experiments.d >101:
                new_experiments.d_status = False  
            else:
                new_experiments.d_status = True
        else:
            new_experiments.d_status = True
        if new_experiments.psa:
            if new_person.age < 40:
                if new_experiments.psa >= 1.7:
                    new_experiments.psa_status = False
                else:
                    new_experiments.psa_status = True
            if new_person.age < 50 or new_person.age >= 40 :
                if new_experiments.psa >= 2.2:
                    new_experiments.psa_status = False
                else:
                    new_experiments.psa_status = True
            if new_person.age < 60 or new_person.age >= 50:
                if new_experiments.psa >= 3.4:
                    new_experiments.psa_status = False
                else:
                    new_experiments.psa_status = True
            if new_person.age < 70 or new_person.age >= 60:
                if new_experiments.psa >= 6.16:
                    new_experiments.psa_status = False
                else:
                    new_experiments.psa_status = True
            if new_person.age > 70:
                if new_experiments.psa >= 6.77:
                    new_experiments.psa_status = False
                else:
                    new_experiments.psa_status = True
            else:
                new_experiments.psa_status = True
        else:
            new_experiments.psa_status = True
        if new_person.gender == 'mard':
            if new_experiments.cbc_rbc:
                if new_experiments.cbc_rbc < 4 or new_experiments.cbc_rbc >6:
                    new_experiments.cbc_rbc_status = False 
                else:
                    new_experiments.cbc_rbc_status = True
            else:
                new_experiments.cbc_rbc_status = True
            if new_experiments.cbc_hb:
                if new_experiments.cbc_hb < 12 or new_experiments.cbc_hb >16:
                    new_experiments.cbc_hb_status = False 
                else:
                    new_experiments.cbc_hb_status = True
            else:
                new_experiments.cbc_hb_status = True
            if new_experiments.cbc_htc:
                if new_experiments.cbc_htc < 40 or new_experiments.cbc_htc >54:
                    new_experiments.cbc_htc_status = False 
                else:
                    new_experiments.cbc_htc_status = True
            else:
                new_experiments.cbc_htc_status = True
            if new_experiments.hdl:
                if new_experiments.hdl > 40:
                    new_experiments.hdl_status = False    
                else:
                    new_experiments.hdl_status = True 
            else:
                new_experiments.hdl_status = True
        if new_person.gender == 'zan':
            if new_experiments.cbc_rbc:
                if new_experiments.cbc_rbc < 3.5 or new_experiments.cbc_rbc >5:
                    new_experiments.cbc_rbc_status = False 
                else:
                    new_experiments.cbc_rbc_status = True
            else:
                new_experiments.cbc_rbc_status = True
            if new_experiments.cbc_hb:
                if new_experiments.cbc_hb < 11 or new_experiments.cbc_hb >15:
                    new_experiments.cbc_hb_status = False 
                else:
                    new_experiments.cbc_hb_status = True
            else:
                new_experiments.cbc_hb_status = True
            if new_experiments.cbc_htc:
                if new_experiments.cbc_htc < 37 or new_experiments.cbc_htc >47:
                    new_experiments.cbc_htc_status = False 
                else:
                    new_experiments.cbc_htc_status = True
            else:
                new_experiments.cbc_htc_status = True
            if new_experiments.hdl:
                if new_experiments.hdl > 50:
                    new_experiments.hdl_status = False    
                else:
                    new_experiments.hdl_status = True  
            else:
                new_experiments.hdl_status = True    
        new_experiments.save()
    if personal_species.is_valid() and  para_clinic.is_valid():
        new_para_clinic = para_clinic.save(commit=False)
        if new_person.examinations_type == 'badv_estekhdam':
            new_para_clinic.opto_hedat_r_ba = 10
            new_para_clinic.opto_hedat_r_bi = 10
            new_para_clinic.opto_hedat_l_ba = 10
            new_para_clinic.opto_hedat_l_bi = 10
        new_para_clinic.person = new_person
        new_para_clinic.save()
    if personal_species.is_valid() and  consulting.is_valid():
        new_consulting = consulting.save(commit=False)
        new_consulting.person = new_person
        new_consulting.save()
    if personal_species.is_valid() and  final_theory.is_valid():
        new_final_theory = final_theory.save(commit=False)
        new_final_theory.person = new_person
        new_final_theory.save() 
    examination_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    inputlist=Personal_Species_Model.objects.filter(examinations_code=examinations_course)
    context={ 'inputlist':inputlist ,'code_list' : code_list ,'form' : form ,'personal_species' : personal_species , 'job_history' : job_history , 'assessment' : assessment, 'personal_history' : personal_history, 'examinations' : examinations, 'experiments' : experiments, 'para_clinic' : para_clinic, 'consulting' : consulting , 'final_theory' : final_theory }
    return render(request, 'edit_examinations.html',context)


@login_required(login_url='login')
def examinations_output_view(request):
    return render(request, 'examinations_output.html')


@require_POST
def examinations_output_edit_add_view(request):
    if Disease_Model:
        model=Disease_Model.objects.last()
    else:
        a = Disease_Model(examinations_code='',order_number=1)
        a.save()
        model=Disease_Model.objects.last()
    form=disease_form(request.POST)
    if form.is_valid():
        if not form.cleaned_data['e_fathers_name']:
            form.cleaned_data['e_fathers_name'] = 'None'
        if not form.cleaned_data['e_personal_code']:
            form.cleaned_data['e_personal_code'] = 0
        model.e_examinations_code=form.cleaned_data['e_examinations_code']
        model.e_name=form.cleaned_data['e_name']
        model.e_fathers_name=form.cleaned_data['e_fathers_name']
        model.e_age=form.cleaned_data['e_age']
        model.e_personal_code=form.cleaned_data['e_personal_code']
        model.save()
    return redirect('examinations_output_edit')

@require_POST
def examinations_output_edit_delete_view(request):
    model=Disease_Model.objects.last()
    code=model.examinations_code
    examinations_course = ExaminationsCourse.objects.filter(examinations_code=code).last()
    qs=Personal_Species_Model.objects.filter(name=model.e_name,age=1401 - model.e_age,fathers_name=model.e_fathers_name,personal_code=model.e_personal_code,examinations_code=examinations_course).last()
    qs.delete()
    return redirect('examinations_output_edit')