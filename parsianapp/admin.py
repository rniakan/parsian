from django.contrib import admin
from .models import Disease_Model,Personal_Species_Model,Job_History_Model,Assessment_Model,Personal_History_Model,Examinations_Model,Experiments_Model,Para_Clinic_Model,Consulting_Model,Final_Theory_Model,Company,ExaminationsCourse

admin.site.register(Disease_Model)
admin.site.register(Personal_Species_Model)
admin.site.register(Job_History_Model)
admin.site.register(Assessment_Model)
admin.site.register(Personal_History_Model)
admin.site.register(Examinations_Model)
admin.site.register(Experiments_Model)
admin.site.register(Para_Clinic_Model)
admin.site.register(Consulting_Model)
admin.site.register(Final_Theory_Model)
admin.site.register(Company)
admin.site.register(ExaminationsCourse)