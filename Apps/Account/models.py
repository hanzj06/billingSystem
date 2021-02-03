import os
from pathlib import Path
from django.db import models
# Create your models here.
from django.db.models import DO_NOTHING
from django.db.models.functions import datetime
from django.utils import timezone

class FirstSubjects(models.Model):
    """
        一级科目表
    """
    fsubcode = models.IntegerField(verbose_name="一级科目编码", unique=True)
    fsubname = models.CharField(max_length=32, verbose_name="一级科目名称", unique=True)
    def __str__(self):
        return "%s(%d)" % (self.fsubname, self.fsubcode)

    class Meta:
        verbose_name = '一级科目'
        verbose_name_plural = "一级科目"

class SecondSubjects(models.Model):
    """
        二级科目表
    """
    ssubcode = models.IntegerField(verbose_name="二级科目编码", unique=True)
    ssubname = models.CharField(max_length=32, verbose_name="二级科目名称", unique=True)
    fathercode = models.ForeignKey("FirstSubjects", to_field="fsubcode", verbose_name="所属一级科目", on_delete=DO_NOTHING)
    def __str__(self):
        return "%s(%d)" % (self.ssubname, self.ssubcode)

    class Meta:
        verbose_name = '二级科目'
        verbose_name_plural = "二级科目"

class DetailSubjects(models.Model):
    """
        明细段表
    """
    dsubcode = models.IntegerField(verbose_name="明细段编码", unique=True)
    dsubname = models.CharField(max_length=64, verbose_name="明细段名称", unique=True)
    def __str__(self):
        return "%s(%d)" % (self.dsubname, self.dsubcode)

    class Meta:
        verbose_name = '明细段'
        verbose_name_plural = "明细段"

class CashSubjects(models.Model):
    """
        现金段表
    """
    csubcode = models.IntegerField(verbose_name="现金段编码", unique=True)
    csubname = models.CharField(max_length=64, verbose_name="现金段名称", unique=True)
    def __str__(self):
        return "%s(%d)" % (self.csubname, self.csubcode)

    class Meta:
        verbose_name = '现金段'
        verbose_name_plural = "现金段"
class AccountingVouchers(models.Model):
    """
        账目表
    """
    recordtime = models.DateField(verbose_name="账目发生日期")
    billtime = models.DateTimeField(default=timezone.now, verbose_name="记账时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    voucherno = models.CharField(max_length=15, unique=True, verbose_name="记账凭证编号")
    abstract = models.CharField(max_length=300, verbose_name="账目摘要", blank=True, null=True)

    debitamount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="借方金额")
    debitfsubcode = models.ForeignKey(to=FirstSubjects, to_field="fsubcode", verbose_name="一级科目(借)",
                                      related_name="dfsubcode", on_delete=DO_NOTHING)
    debitssubcode = models.ForeignKey(to=SecondSubjects, to_field="ssubcode",  verbose_name="二级科目(借)",
                                      blank=True, null=True, related_name="dssubcode", on_delete=DO_NOTHING)
    debitdsubcode = models.ForeignKey(to=DetailSubjects, to_field="dsubcode", verbose_name="明细科目(借)",
                                      blank=True, null=True, related_name="ddsubcode", on_delete=DO_NOTHING)

    creditamount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="贷方金额")
    creditfsubcode = models.ForeignKey(to=FirstSubjects, to_field="fsubcode", verbose_name="一级科目(贷)",
                                       related_name="cfsubcode", on_delete=DO_NOTHING)
    creditssubcode = models.ForeignKey(to=SecondSubjects, to_field="ssubcode", verbose_name="二级科目(贷)",
                                       blank=True, null=True, related_name="cssubcode", on_delete=DO_NOTHING)
    creditdsubcode = models.ForeignKey(to=DetailSubjects, to_field="dsubcode", verbose_name="明细科目(贷)",
                                       blank=True, null=True, related_name="cdsubcode", on_delete=DO_NOTHING)


    # operatertypeChoices = (
    #     (0, "会计主管"),
    #     (1, "记账"),
    #     (2, "出纳"),
    #     (3, "复核"),
    #     (4, "制单"),
    # )
    # operatertype = models.SmallIntegerField(choices=operatertypeChoices, default=1, verbose_name="操作者角色")
    operatername = models.CharField(max_length=10, verbose_name="录入者")
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    url = r"upload\{time}".format(time=now_time)
    uploadurl = os.path.join(BASE_DIR, url)
    voucherfile = models.FileField(upload_to=uploadurl, blank=True, null=True, verbose_name="附件")

    def short_abstract(self):
        if len(str(self.abstract)) > 30:
            return ['{}...'.format(str(self.abstract)[0:29]), self.abstract]
        else:
            return str(self.abstract)
    short_abstract.allow_tags = True
    short_abstract.short_description = '记录摘要'

    def short_voucherfile(self):
        if len(str(self.voucherfile)) > 30:
            return ['{}...'.format(str(self.voucherfile)[0:10]), str(self.voucherfile)]
        else:
            return str(self.voucherfile)
    short_voucherfile.allow_tags = True
    short_voucherfile.short_description = '附件'

    class Meta:
        verbose_name = '账目'
        verbose_name_plural = "账目登记"

# 以下是修改后的数据表
class SubjectType(models.Model):
    """
        科目类别表
    """
    id = models.SmallIntegerField(verbose_name="科目类别", unique=True, primary_key=True)
    des = models.CharField(max_length=32, verbose_name="类别描述")
    def __str__(self):
        return "%s(%d)" % (self.des, self.id)

    class Meta:
        verbose_name = '科目类别'
        verbose_name_plural = "科目类别"

class SubjectCategory(models.Model):
    """
        账户种类表
    """
    id = models.SmallIntegerField(verbose_name="种类ID", unique=True, primary_key=True)
    des = models.CharField(max_length=32, verbose_name="描述")
    def __str__(self):
        return "%s(%d)" % (self.des, self.id)

    class Meta:
        verbose_name = '账户种类'
        verbose_name_plural = "账户种类"

class Subjects(models.Model):
    """
        科目结构表
    """
    subtype = models.ForeignKey(to=SubjectType, to_field='id', verbose_name='科目类别', on_delete=DO_NOTHING)
    subcode = models.CharField(max_length=20, verbose_name="科目编码", unique=True)
    subdescription = models.CharField(max_length=128, verbose_name="科目说明")
    substatus = models.BooleanField(verbose_name="是否启用", default=True)
    needsummary = models.BooleanField(verbose_name="是否需要汇总", default=False)
    level = models.SmallIntegerField(verbose_name="层级", blank=True, null=True)
    category = models.ForeignKey(to=SubjectCategory, to_field='id', verbose_name="账户种类", blank=True, null=True, on_delete=DO_NOTHING)
    def __str__(self):
        return "%s(%s)" % (self.subdescription, self.subcode)

    class Meta:
        verbose_name = '科目结构'
        verbose_name_plural = "科目结构"


class AccountBaseInfo(models.Model):
    """
        账目基本信息表
    """
    recordtime = models.DateField(verbose_name="账目日期")
    billtime = models.DateTimeField(default=timezone.now, verbose_name="记账时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    voucherno = models.CharField(max_length=15, unique=True, verbose_name="凭证号")
    debittotal = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="借方总金额")
    credittotal = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="贷方总金额")
    biller = models.CharField(max_length=10, verbose_name="入账人")
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    url = r"upload\{time}".format(time=now_time)
    uploadurl = os.path.join(BASE_DIR, url)
    voucherfile = models.FileField(upload_to=uploadurl, blank=True, null=True, verbose_name="附件")
    def short_voucherfile(self):
        if len(str(self.voucherfile)) > 30:
            return ['{}...'.format(str(self.voucherfile)[0:10]), str(self.voucherfile)]
        else:
            return str(self.voucherfile)
    short_voucherfile.allow_tags = True
    short_voucherfile.short_description = '附件'

    class Meta:
        verbose_name = '账目基本信息'
        verbose_name_plural = "账目基本信息"

class AccountDetail(models.Model):
    """
        账目明细表
    """
    voucherno = models.ForeignKey(to=AccountBaseInfo, to_field='voucherno', verbose_name='凭证号',
                                  related_name='VNO', on_delete=DO_NOTHING)
    abstract = models.CharField(max_length=128, verbose_name='摘要')
    subcodeset = models.CharField(max_length=128, verbose_name='科目编码')
    fsubcode = models.CharField(max_length=32, verbose_name='一级科目', blank=True, null=True)
    ssubcode = models.CharField(max_length=32, verbose_name='二级科目', blank=True, null=True)
    csubcode = models.CharField(max_length=32, verbose_name='现金段', blank=True, null=True)
    dsubcode = models.CharField(max_length=32, verbose_name='明细段', blank=True, null=True)
    debitamount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='借方金额', blank=True, null=True)
    creditamount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='贷方金额', blank=True, null=True)
    class Meta:
        verbose_name = '账目明细表'
        verbose_name_plural = "账目明细表"
