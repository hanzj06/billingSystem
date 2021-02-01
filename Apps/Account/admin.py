from django.contrib import admin


# Register your models here.
from .models import AccountingVouchers, FirstSubjects, SecondSubjects, DetailSubjects, Subjects, SubjectType, \
    SubjectCategory, AccountDetail, AccountBaseInfo


@admin.register(AccountingVouchers)
class AccountingVouchersAdmin(admin.ModelAdmin):
    list_display = ["recordtime", "voucherno", "short_abstract",
                    "debitamount", "debitfsubcode", "debitssubcode", "debitdsubcode",
                    "creditamount", "creditfsubcode", "creditssubcode", "creditdsubcode",
                    "operatername", "short_voucherfile", "billtime", "updatetime"]
# admin.site.register(AccountingVouchers, AccountingVouchersAdmin)
admin.site.site_title = "合肥速率供应链管理有限公司"
admin.site.site_header = "后台录入系统"



class SecondSubjectsItem(admin.TabularInline):
    model = SecondSubjects
    extra = 1

@admin.register(FirstSubjects)
class FirstSubjectsAdmin(admin.ModelAdmin):
    inlines = [SecondSubjectsItem]
    list_display = ["fsubcode", "fsubname"]
# admin.site.register(FirstSubjects, FirstSubjectsAdmin)

@admin.register(SecondSubjects)
class SecondSubjectsAdmin(admin.ModelAdmin):
    list_display = ["ssubcode", "ssubname", "fathercode"]
    list_filter = ["fathercode"]

@admin.register(DetailSubjects)
class DetailSubjectsAdmin(admin.ModelAdmin):
    list_display = ["dsubcode", "dsubname"]
# 以下是修改后
@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ["subtype", "subcode", "subdescription", "substatus", "needsummary", "level", "category"]

@admin.register(SubjectType)
class SubjectTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "des"]

@admin.register(SubjectCategory)
class SubjectCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "des"]

class AccountDetailItem(admin.TabularInline):
    model = AccountDetail
    extra = 5

@admin.register(AccountBaseInfo)
class AccountBaseInfoAdmin(admin.ModelAdmin):
    inlines = [AccountDetailItem]
    list_display = ["recordtime", "voucherno", "debittotal", "credittotal", "biller", "voucherfile", "billtime", "updatetime"]

@admin.register(AccountDetail)
class AccountDetailAdmin(admin.ModelAdmin):
    list_display = ["voucherno", "abstract", "subcodeset", "debitamount", "creditamount"]

