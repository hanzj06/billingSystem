from django.contrib import admin

# Register your models here.
from .models import CompanyBaseInfo
@admin.register(CompanyBaseInfo)
class CompanyBaseInfoAdmin(admin.ModelAdmin):
    # 列表页自定义
    list_display = ["companyname", "bankname", "bankID", "beginningbalances"]
    # 新增，修改页自定义
    fields = []
    fieldsets = []
# admin.site.register(CompanyBaseInfo, CompanyBaseInfoAdmin)


# admin.site.register(SecondSubjects, SecondSubjectsAdmin)
