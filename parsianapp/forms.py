from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Disease_Model, Personal_Species_Model, Job_History_Model, Assessment_Model, Personal_History_Model, \
    Examinations_Model, Experiments_Model, Para_Clinic_Model, Consulting_Model, Final_Theory_Model, Company, \
    ExaminationsCourse


class registration(UserCreationForm):
    class meta:
        model = User
        fields = ['username', 'password']


class submit_company_form(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'company': forms.TextInput(attrs={'autocomplete': 'off', })}


class ExaminationsCompanyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

#  ثبت دوره معاینات
class submit_course_form(forms.ModelForm):
    # company: ExaminationsCompanyChoiceField(queryset=Company.objects.all())
    class Meta:
        model = ExaminationsCourse
        fields = '__all__'
        widgets = {
            'year': forms.NumberInput(attrs={'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'company': forms.TextInput(attrs={'autocomplete': 'off', 'list': 'company'}),
            'doctor': forms.TextInput(attrs={'autocomplete': 'off'}),
            'employer': forms.TextInput(attrs={'autocomplete': 'off'}),
            'examinations_code': forms.TextInput(attrs={'autocomplete': 'off'})}


class disease_form(forms.ModelForm):
    class Meta:
        model = Disease_Model
        fields = '__all__'
        widgets = {'examinations_code': forms.TextInput(attrs={'autocomplete': 'off', 'list': 'examinations_code'})
            , 'order_number': forms.Select(attrs={'autocomplete': 'off'})
            , 'age': forms.NumberInput(attrs={'class': 'box', 'autocomplete': 'off'})
            , 'name': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'})
            , 'fathers_name': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'})
            , 'personal_code': forms.NumberInput(attrs={'class': 'personal_w', 'autocomplete': 'off'})
            , 'p_age': forms.NumberInput(attrs={'style': 'width : 100px', 'autocomplete': 'off', 'list': 'age'})
            , 'p_name': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off', 'list': 'name'})
            , 'p_fathers_name': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off', 'list': 'fathers_name'})
            , 'p_personal_code': forms.NumberInput(
                attrs={'class': 'personal_w', 'autocomplete': 'off', 'list': 'personal_code'})
            , 'p_examinations_code': forms.TextInput(attrs={'autocomplete': 'off', 'list': 'examinations_code'})
            , 'e_age': forms.NumberInput(attrs={'style': 'width : 100px', 'autocomplete': 'off', 'list': 'age'})
            , 'e_name': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off', 'list': 'name'})
            , 'e_fathers_name': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off', 'list': 'fathers_name'})
            , 'e_personal_code': forms.NumberInput(
                attrs={'class': 'personal_w', 'autocomplete': 'off', 'list': 'personal_code'})
            , 'e_examinations_code': forms.TextInput(attrs={'autocomplete': 'off', 'list': 'examinations_code'})
                   }

# مشخصات فردی شاغل
class personal_species_form(forms.ModelForm):
    # examinations_code = ExaminationsCourseChoiceField(queryset=ExaminationsCourse.objects.all())
    class Meta:
        model = Personal_Species_Model
        fields = '__all__'
        widgets = {
            'species_date_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'examinations_code': forms.TextInput(
                attrs={'class': 'text', 'autocomplete': 'off', "required": 'True', 'list': 'examinations_code'}),
            'examinations_type': forms.Select(attrs={'class': 'text', 'autocomplete': 'off'}),
            'profil_number': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'employment_number': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'name': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off', "required": 'True'}),
            'fathers_name': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'gender': forms.Select(attrs={'class': 's_box', 'autocomplete': 'off', 'id': 'select', "required": 'True'}),
            'marriage_status': forms.Select(attrs={'class': 'box', 'autocomplete': 'off'}),
            'children': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'age': forms.NumberInput(attrs={'class': 'box', 'autocomplete': 'off', "required": 'True', 'min': '1300', 'max': '1500'}),
            'personal_code': forms.NumberInput(attrs={'class': 'personal_w', 'autocomplete': 'off', 'min': '99999', 'max': '99999999999'}),
            'military_status': forms.Select(attrs={'class': 'text', 'autocomplete': 'off'}),
            'raste': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'medical_exemption': forms.Select(attrs={'class': 'text', 'autocomplete': 'off'}),
            'medical_exemption_reason': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'job_name': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'employer_name': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'address': forms.TextInput(attrs={'style': 'width : 800px', 'autocomplete': 'off'}),
            'species_date_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'species_date_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'})
        }

    def clean_test_value(self):
        data = self.cleaned_data.get('date_day')
        if data:
            return data
        else:
            raise forms.ValidationError('کد معاینات پر نشده است')

# سوابق شغلی
class job_history_form(forms.ModelForm):
    class Meta:
        model = Job_History_Model
        fields = '__all__'
        widgets = {
            # current job
            'first_current_job': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'first_current_job_duty': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'first_current_job_from_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'first_current_job_from_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'first_current_job_to_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'first_current_job_to_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'first_current_change_job_reason': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'second_current_job': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'second_current_job_duty': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'second_current_job_from_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'second_current_job_from_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'second_current_job_to_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'second_current_job_to_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'second_current_change_job_reason': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            # previous job
            'first_previous_job': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'first_previous_job_duty': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'first_previous_job_from': forms.TextInput(attrs={'class': 'date_year', 'autocomplete': 'off'}),
            'first_previous_job_to': forms.TextInput(attrs={'class': 'date_year', 'autocomplete': 'off'}),
            'first_previous_change_job_reason': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'second_previous_job': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'second_previous_job_duty': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'}),
            'second_previous_job_from': forms.TextInput(attrs={'class': 'date_year', 'autocomplete': 'off'}),
            'second_previous_job_to': forms.TextInput(attrs={'class': 'date_year', 'autocomplete': 'off'}),
            'second_previous_change_job_reason': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off'})
        }


class assessment_form(forms.ModelForm):
    class Meta:
        model = Assessment_Model
        fields = '__all__'
        widgets = {
            'required_description': forms.TextInput(attrs={'autocomplete': 'off', 'style': 'width:52%'}),
            'kar_shenas': forms.TextInput(attrs={'autocomplete': 'off', 'style': 'width:65%'}),
            'ass_date_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'ass_date_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'ass_date_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'})
        }

# سابقه شخصی,خانوادگی و پزشکی
class personal_history_form(forms.ModelForm):
    class Meta:
        model = Personal_History_Model
        fields = '__all__'
        widgets = {
            'first_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'first_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'}),
            'second_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'third_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'fourth_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'fifth_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'fifth_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'}),
            'sixth_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'sixth_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'}),
            'seventh_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'seventh_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'}),
            'eighth_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'eighth_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'}),
            'ninth_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'ninth_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'}),
            'twelfth_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'twelfth_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'}),
            'thirteenth_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'}),
            'fourteenth_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'fourteenth_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'}),
            'fifteenth_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'fifteenth_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'}),
            'sixteenth_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'sixteenth_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'}),
            'tenth_des_number': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'tenth_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'}),
            'eleventh_des_number': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'eleventh_n': forms.CheckboxInput(attrs={'autocomplete': 'off', 'checked': 'true'})
        }

#   معاینات
class examinations_form(forms.ModelForm):
    class Meta:
        model = Examinations_Model
        fields = '__all__'
        widgets = {
            'local_sym_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'local_sign_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'eye_sym_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'eye_sign_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'skin_sym_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'skin_sign_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'gosh_sym_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'gosh_sign_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'sar_sym_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'sar_sign_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'rie_sym_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'rie_sign_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'ghalb_sym_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'ghalb_sign_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'shekam_sym_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'shekam_sign_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'colie_sym_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'colie_sign_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'eskelety_sym_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'eskelety_sign_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'asabi_sym_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'asabi_sign_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'ravan_sym_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'ravan_sign_without_sign': forms.CheckboxInput(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'checked': 'true'}),
            'local_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'eye_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'skin_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'gosh_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'sar_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'rie_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'ghalb_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'shekam_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'colie_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'eskelety_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'asabi_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'ravan_des': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'weight': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '10', 'max': '250'}),
            'other': forms.TextInput(attrs={'autocomplete': 'off', 'style': 'width:100%'}),
            'min_blood_pressure': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '25'}),
            'max_blood_pressure': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'}),
            'length': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '50', 'max': '300'}),
            'pulse': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'exa_date_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'exa_date_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'exa_date_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'})
        }

#  آزمایش ها
class experiments_form(forms.ModelForm):
    class Meta:
        model = Experiments_Model
        fields = '__all__'
        widgets = {
            'cbc_wbc': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'cbc_rbc': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'date_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off'}),
            'cbc_hb': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'cbc_htc': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'cbc_plt': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'ua_prot': forms.NumberInput(
                attrs={'class': 'examination_box ua', 'autocomplete': 'off', 'step': '0.00001'}),
            'ua_glu': forms.NumberInput(
                attrs={'class': 'examination_box ua', 'autocomplete': 'off', 'step': '0.00001'}),
            'ua_rbc': forms.NumberInput(
                attrs={'class': 'examination_box ua', 'autocomplete': 'off', 'step': '0.00001'}),
            'ua_wbc': forms.NumberInput(
                attrs={'class': 'examination_box ua', 'autocomplete': 'off', 'step': '0.00001'}),
            'ua_bact': forms.NumberInput(
                attrs={'class': 'examination_box ua', 'autocomplete': 'off', 'step': '0.00001'}),
            'fbs': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'chol': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'ldl': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'hdl': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'tg': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'lead': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'cr': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'alt': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'd': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'tsh': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'ast': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'alk': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'psa': forms.NumberInput(attrs={'class': 'examination_box', 'autocomplete': 'off', 'step': '0.00001'}),
            'first_date_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'first_date_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'first_date_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'}),
            'second_date_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'second_date_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'second_date_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'}),
            'third_date_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'third_date_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'third_date_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'}),
            'exp_date_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'exp_date_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'exp_date_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'})
        }

# پاراکلینیک
class para_clinic_form(forms.ModelForm):
    class Meta:
        model = Para_Clinic_Model
        fields = '__all__'
        widgets = {
            'opto_date_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'opto_date_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'opto_date_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'}),
            'opto_hedat_r_ba': forms.NumberInput(
                attrs={'class': 's_box auto-filler', 'autocomplete': 'off', 'disabled': 'disabled'}),
            'opto_hedat_r_bi': forms.NumberInput(
                attrs={'class': 's_box auto-filler', 'autocomplete': 'off', 'disabled': 'disabled'}),
            'opto_hedat_r_status': forms.Select(
                attrs={'autocomplete': 'off', 'class': 'auto-filler', 'onchange': "toggleInput();"}),
            'opto_hedat_l_ba': forms.NumberInput(
                attrs={'class': 's_box auto-filler', 'autocomplete': 'off', 'disabled': 'disabled'}),
            'opto_hedat_l_bi': forms.NumberInput(
                attrs={'class': 's_box auto-filler', 'autocomplete': 'off', 'disabled': 'disabled'}),
            'opto_hedat_l_status': forms.Select(
                attrs={'class': 'auto-filler', 'autocomplete': 'off', 'onchange': "toggleInput();"}),
            'opto_rangi_hedat_r_ba': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'opto_rangi_hedat_r_bi': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'opto_rangi_hedat_l_ba': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'opto_rangi_hedat_l_bi': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'opto_meidan_hedat_r_ba': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'opto_meidan_hedat_r_bi': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'opto_meidan_hedat_l_ba': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'opto_meidan_hedat_l_bi': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'opto_omgh': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off'}),
            'opto_Description': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'audio_date_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'audio_date_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'audio_r_tafsir': forms.Select(attrs={'class': 'auto-filler', 'autocomplete': 'off'}),
            'audio_l_tafsir': forms.Select(attrs={'class': 'auto-filler', 'autocomplete': 'off'}),
            'audio_date_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'}),
            'audio_r_eight_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_eight_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_six_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_six_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_four_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_four_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_three_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_three_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_two_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_two_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_one_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_one_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_five_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_r_five_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_eight_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_eight_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_six_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_six_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_four_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_four_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_three_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_three_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_two_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_two_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_one_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_one_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_five_ac': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'audio_l_five_bc': forms.NumberInput(attrs={'class': 's_box auto-filler', 'autocomplete': 'off'}),
            'espiro_date_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'espiro_date_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'espiro_date_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'}),
            'espiro_tafsir': forms.Select(attrs={'autocomplete': 'off'}),
            'espiro_fevvfvc': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'espiro_fev': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'espiro_fvc': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'espiro_vext': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'espiro_pef': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'espiro_fef': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'other_cxr_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'other_cxr_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'other_cxr_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'}),
            'other_ecg_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'other_ecg_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'other_ecg_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'}),
            'description_ecg': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off', 'style': 'width : 75%'}),
            'description_cxr': forms.TextInput(attrs={'class': 'text', 'autocomplete': 'off', 'style': 'width : 75%'}),
            'other_result': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'})
        }

#  قبت مشاوره ها و نتایح ارجاع
class consulting_form(forms.ModelForm):
    class Meta:
        model = Consulting_Model
        fields = '__all__'
        widgets = {
            'first_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'first_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'first_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'}),
            'second_year': forms.NumberInput(attrs={'class': 'date_year', 'autocomplete': 'off', 'min': '1300', 'max': '1500'}),
            'second_month': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '12'}),
            'first_result': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'second_result': forms.TextInput(attrs={'class': 'des', 'autocomplete': 'off'}),
            'second_day': forms.NumberInput(attrs={'class': 's_box', 'autocomplete': 'off', 'min': '1', 'max': '30'})
        }

#  نظریه نهایی پزشک متخصص طب کار
class final_theory_form(forms.ModelForm):
    class Meta:
        model = Final_Theory_Model
        fields = '__all__'
        widgets = {
            'mashrot_reason': forms.TextInput(attrs={'autocomplete': 'off', 'style': 'width : 91%'}),
            'rad_reason': forms.TextInput(attrs={'autocomplete': 'off', 'style': 'width : 84%'}),
            'recommendations': forms.TextInput(attrs={'autocomplete': 'off', 'style': 'width : 95%'}),
            'reason': forms.TextInput(attrs={'autocomplete': 'off', 'style': 'width : 95%'}),
            'problems': forms.TextInput(attrs={'autocomplete': 'off', 'style': 'width : 70%'}),
            'd_code': forms.NumberInput(attrs={'autocomplete': 'off', 'class': 'box'})
        }
