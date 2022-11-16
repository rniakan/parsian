from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Disease_Model,Personal_Species_Model,Job_History_Model,Assessment_Model,Personal_History_Model,Examinations_Model,Experiments_Model,Para_Clinic_Model,Consulting_Model,Final_Theory_Model,Company,ExaminationsCourse
from . import models
from django.core.validators import MaxValueValidator, MinValueValidator 
class registration(UserCreationForm):
    class meta:
        model=User
        fields=['username','password']

        
class submit_company_form(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets={
        'company' : forms.TextInput(attrs={'autocomplete': 'off' , })}

class ExaminationsCompanyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name

class submit_course_form(forms.ModelForm):
    company : ExaminationsCompanyChoiceField(queryset=Company.objects.all())
    class Meta:
        model = ExaminationsCourse
        fields = '__all__'
        widgets={
        'year' : forms.TextInput(attrs={'autocomplete': 'off' }),
        'doctor' : forms.TextInput(attrs={'autocomplete': 'off' }),
        'employer' : forms.TextInput(attrs={'autocomplete': 'off' }),
        'examinations_code' : forms.TextInput(attrs={'autocomplete': 'off' })}

class disease_form(forms.ModelForm):
    class Meta:
        model=Disease_Model
        fields='__all__'
        widgets={'examinations_code' : forms.TextInput(attrs={'autocomplete': 'off','list':'examinations_code'})
        ,'order_number' : forms.Select(attrs={'autocomplete': 'off'})
        ,'age' : forms.NumberInput(attrs={'class':'box','autocomplete': 'off'})
        ,'name' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'})
        ,'fathers_name' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'})
        ,'personal_code' : forms.NumberInput(attrs={'class':'personal_w','autocomplete': 'off'})
        ,'p_age' : forms.NumberInput(attrs={'class':'box','autocomplete': 'off'})
        ,'p_name' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'})
        ,'p_fathers_name' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'})
        ,'p_personal_code' : forms.NumberInput(attrs={'class':'personal_w','autocomplete': 'off'})
        ,'p_examinations_code' : forms.TextInput(attrs={'autocomplete': 'off','list':'examinations_code'})
        ,'e_age' : forms.NumberInput(attrs={'class':'box','autocomplete': 'off'})
        ,'e_name' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'})
        ,'e_fathers_name' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'})
        ,'e_personal_code' : forms.NumberInput(attrs={'class':'personal_w','autocomplete': 'off'})
        ,'e_examinations_code' : forms.TextInput(attrs={'autocomplete': 'off','list':'examinations_code'})
        }  

class ExaminationsCourseChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.examinations_code

class personal_species_form(forms.ModelForm):
    examinations_code = ExaminationsCourseChoiceField(queryset=ExaminationsCourse.objects.all())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['examinations_code'].required = True
    class Meta:
        model=Personal_Species_Model
        fields='__all__' 
        widgets={
        'species_date_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'examinations_type' : forms.Select(attrs={'class':'text','autocomplete': 'off'}),
        'profil_number' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'employment_number' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'name' : forms.TextInput(attrs={'class':'text','autocomplete': 'off',"required": 'True'}),
        'fathers_name' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'}),
        'gender' : forms.Select(attrs={'class':'s_box','autocomplete': 'off','id':'select',"required": 'True'}),
        'marriage_status' : forms.Select(attrs={'class':'box','autocomplete': 'off'}),
        'children' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'age' : forms.NumberInput(attrs={'class':'box','autocomplete': 'off',"required": 'True'}),
        'personal_code' : forms.NumberInput(attrs={'class':'personal_w','autocomplete': 'off'}),
        'military_status' : forms.Select(attrs={'class':'text','autocomplete': 'off'}),
        'raste' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'}),
        'medical_exemption' : forms.Select(attrs={'class':'text','autocomplete': 'off'}),
        'medical_exemption_reason' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'}),
        'job_name' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'}),
        'employer_name' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'}),
        'address' : forms.TextInput(attrs={'style':'width : 800px','autocomplete': 'off'}),
        'species_date_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'species_date_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'})
        }
    def clean_test_value(self):
        data = self.cleaned_data.get('date_day')
        if data:
            return data
        else:
            raise form.ValidationError('کد معاینات پر نشده است')

class job_history_form(forms.ModelForm):
    class Meta:
        model=Job_History_Model
        fields='__all__' 
        widgets={
        'current_job' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'}),
        'current_job_duty' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'}),
        'current_job_from_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'current_job_from_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'current_job_to_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'current_job_to_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'current_job_reason' : forms.TextInput(attrs={'class':'text','autocomplete': 'off'}),
        'second_current_job' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'second_current_job_duty' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'second_current_job_from' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'second_current_job_to' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'second_current_job_reason' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'previous_job' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'previous_job_duty' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'previous_job_from' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'previous_job_to' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'previous_job_reason' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'second_previous_job' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'second_previous_job_duty' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'second_previous_job_from' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'second_previous_job_to' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'}),
        'second_previous_job_reason' : forms.TextInput(attrs={'class':'text remove','autocomplete': 'off'})
        }

class assessment_form(forms.ModelForm):
    class Meta:
        model=Assessment_Model
        fields='__all__' 
        widgets={
        'required_description' : forms.TextInput(attrs={'autocomplete': 'off','style':'width:52%'}),
        'kar_shenas' : forms.TextInput(attrs={'autocomplete': 'off','style':'width:65%'}),
        'ass_date_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'ass_date_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'ass_date_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'})
        }
        
class personal_history_form(forms.ModelForm):
    class Meta:
        model=Personal_History_Model
        fields='__all__' 
        widgets={
        'first_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'second_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'third_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'fourth_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'fifth_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'sixth_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'seventh_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'eighth_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'ninth_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'twelfth_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'fourteenth_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'fifteenth_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'sixteenth_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'tenth_des_number' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'eleventh_des_number' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'})
        }
class examinations_form(forms.ModelForm):
    class Meta:
        model=Examinations_Model
        fields='__all__' 
        widgets={
        'local_sym_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'local_sign_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'eye_sym_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'eye_sign_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'skin_sym_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'skin_sign_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'gosh_sym_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'gosh_sign_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'sar_sym_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'sar_sign_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'rie_sym_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'rie_sign_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'ghalb_sym_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'ghalb_sign_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'shekam_sym_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'shekam_sign_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'colie_sym_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'colie_sign_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'eskelety_sym_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'eskelety_sign_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'asabi_sym_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'asabi_sign_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'ravan_sym_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'ravan_sign_without_sign' : forms.CheckboxInput(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'local_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'eye_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'skin_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'gosh_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'sar_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'rie_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'ghalb_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'shekam_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'colie_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'eskelety_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'asabi_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'ravan_des' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'weight' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'other' : forms.TextInput(attrs={'autocomplete': 'off','style':'width:100%'}),
        'blood_pressure' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'length' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'pulse' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'exa_date_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'exa_date_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'exa_date_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'})
        }

class experiments_form(forms.ModelForm):
    class Meta:
        model=Experiments_Model
        fields='__all__' 
        widgets={
        'cbc_wbc' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'cbc_rbc' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'date_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'cbc_hb' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'cbc_htc' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'cbc_plt' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'ua_prot' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'ua_glu' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'ua_rbc' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'ua_wbc' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'ua_bact' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'fbs' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'chol' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'ldl' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'hdl' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'tg' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'lead' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'cr' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'alt' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'd' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'tsh' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'ast' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'alk' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'psa' : forms.NumberInput(attrs={'class':'examination_box','autocomplete': 'off'}),
        'first_date_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'first_date_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'first_date_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'second_date_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'second_date_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'second_date_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'third_date_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'third_date_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'third_date_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'exp_date_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'exp_date_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'exp_date_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'})
        }

class para_clinic_form(forms.ModelForm):
    class Meta:
        model=Para_Clinic_Model
        fields='__all__' 
        widgets={
        'opto_date_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'opto_date_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'opto_date_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'opto_hedat_r_ba' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off','disabled':'disabled'}),
        'opto_hedat_r_bi' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off','disabled':'disabled'}),
        'opto_hedat_r_status' : forms.Select(attrs={'autocomplete': 'off', 'class':'auto-filler','onchange':"toggleInput();"}),
        'opto_hedat_l_ba' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off','disabled':'disabled'}),
        'opto_hedat_l_bi' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off','disabled':'disabled'}),
        'opto_hedat_l_status' : forms.Select(attrs={'class':'auto-filler','autocomplete': 'off','onchange':"toggleInput();"}),
        'opto_rangi_hedat_r_ba' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'opto_rangi_hedat_r_bi' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'opto_rangi_hedat_l_ba' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'opto_rangi_hedat_l_bi' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'opto_meidan_hedat_r_ba' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'opto_meidan_hedat_r_bi' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'opto_meidan_hedat_l_ba' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'opto_meidan_hedat_l_bi' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'opto_omgh' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'audio_date_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'audio_date_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'audio_r_tafsir' : forms.Select(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'audio_l_tafsir' : forms.Select(attrs={'class':'auto-filler','autocomplete': 'off'}),
        'audio_date_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'audio_r_eight_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_eight_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_six_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_six_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_four_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_four_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_three_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_three_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_two_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_two_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_one_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_one_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_five_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_r_five_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_eight_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_eight_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_six_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_six_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_four_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_four_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_three_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_three_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_two_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_two_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_one_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_one_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_five_ac' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'audio_l_five_bc' : forms.NumberInput(attrs={'class':'s_box auto-filler','autocomplete': 'off'}),
        'espiro_date_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'espiro_date_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'espiro_date_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'espiro_tafsir' : forms.Select(attrs={'autocomplete': 'off'}),
        'espiro_fevvfvc' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'espiro_fev' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'espiro_fvc' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'espiro_vext' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'espiro_pef' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'espiro_fef' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'other_cxr_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'other_cxr_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'other_cxr_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'other_ecg_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'other_ecg_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'other_result' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'other_ecg_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'})
        }

class consulting_form(forms.ModelForm):
    class Meta:
        model=Consulting_Model
        fields='__all__' 
        widgets={
        'first_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'first_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'first_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'second_year' : forms.NumberInput(attrs={'class':'date_year','autocomplete': 'off'}),
        'second_month' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'}),
        'first_result' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'second_result' : forms.TextInput(attrs={'class':'des','autocomplete': 'off'}),
        'second_day' : forms.NumberInput(attrs={'class':'s_box','autocomplete': 'off'})
        }

class final_theory_form(forms.ModelForm):
    class Meta:
        model=Final_Theory_Model
        fields='__all__' 
        widgets={
        'mashrot_reason' : forms.TextInput(attrs={'autocomplete': 'off','style':'width : 91%'}),
        'rad_reason' : forms.TextInput(attrs={'autocomplete': 'off','style':'width : 84%'}),
        'recommendations' : forms.TextInput(attrs={'autocomplete': 'off','style':'width : 95%'}),
        'reason' : forms.TextInput(attrs={'autocomplete': 'off','style':'width : 95%'}),
        'problems' : forms.TextInput(attrs={'autocomplete': 'off','style':'width : 70%'}),
        'd_code' : forms.NumberInput(attrs={'autocomplete': 'off','class':'box'})
        }




