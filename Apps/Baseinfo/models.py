from django.db import models

# Create your models here.
from django.db.models import DO_NOTHING
class CompanyBaseInfo(models.Model):
    """
        公司基本信息表
    """
    companyname = models.CharField(max_length=64, default="合肥速率供应链管理有限公司", verbose_name="公司名称")
    bankname = models.CharField(max_length=64, default="中国银行肥东支行", verbose_name="开户行")
    bankID = models.CharField(max_length=64, unique=True, default="185758792231",  verbose_name="银行账号")
    beginningbalances = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name="期初余额")

    class Meta:
        verbose_name = '基本信息'
        verbose_name_plural = "公司基本信息"
