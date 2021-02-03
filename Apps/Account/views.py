import json
import datetime
import operator
import os
from functools import reduce

import numpy as np
import xlrd
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Apps.Account.models import AccountDetail
from Apps.Baseinfo import models
from Apps.Account import models
from BillingSystem import settings


# Create your views here.
# 测试
def test(request):
    return HttpResponse("Hello")


# 获取一级科目（旧）
def getFirstsubjects(request):
    fsublist = models.FirstSubjects.objects.all()
    fsub_dicts = []
    count = 0
    for fsub in fsublist:
        fsub_dic = {'fsubcode': fsub.fsubcode, 'fsubname': fsub.fsubname}
        fsub_dicts.append(fsub_dic)
        count += 1
    res = {
        'code': 0,
        'msg': 'success',
        'count': count,
        'data': fsub_dicts

    }
    return JsonResponse(res, safe=False)


# 获取二级科目数据（旧）,不带上级code则返回全部数据，带上级code则返回对应的数据
def getSecondSubjects(request):
    if request.GET.get('fathercode') is None or (request.GET.get('fathercode') == ''):
        ssublist = models.SecondSubjects.objects.all()
    else:
        fathercode = request.GET.get('fathercode')
        qs = models.FirstSubjects.objects.filter(fsubcode=fathercode).first()
        ssublist = models.SecondSubjects.objects.filter(fathercode=qs)
    ssub_dicts = []
    count = 0
    for ssub in ssublist:
        ssub_dic = {'ssubcode': ssub.ssubcode, 'ssubname': ssub.ssubname, 'fathercode': ssub.fathercode.fsubcode,
                    'fathername': ssub.fathercode.fsubname}
        ssub_dicts.append(ssub_dic)
        count += 1
    res = {
        'code': 0,
        'msg': 'success',
        'count': count,
        'data': ssub_dicts

    }
    return JsonResponse(res, safe=False)


# 获取并展示所有科目数据（旧）,不带上级code则返回全部数据，带上级code则返回对应的数据
def getSubjectsOld(request):
    sub_dicts = []
    count = 0
    firstSubList = models.FirstSubjects.objects.all()
    for fsub in firstSubList:
        secondSubList = models.SecondSubjects.objects.filter(fathercode=fsub)
        if len(secondSubList) == 0:
            sub_dic = {'ssubcode': None, 'ssubname': '', 'fathercode': fsub.fsubcode,
                       'fathername': fsub.fsubname}
            sub_dicts.append(sub_dic)
            count += 1
        else:
            for ssub in secondSubList:
                sub_dic = {'ssubcode': ssub.ssubcode, 'ssubname': ssub.ssubname,
                           'fathercode': fsub.fsubcode,
                           'fathername': fsub.fsubname}
                sub_dicts.append(sub_dic)
                count += 1
    res = {
        'code': 0,
        'msg': 'success',
        'count': count,
        'data': sub_dicts

    }
    return JsonResponse(res, safe=False)


# ------------------------------以下------------------------------------#

# 获取科目类别数据，以便在请求科目结构的时候知道要请求多少类别
def getSubjectType(request):
    subjectTypeList = models.SubjectType.objects.all()
    subjectType_dicts = []
    count = 0
    for st in subjectTypeList:
        subjectType_dic = {'id': st.id, 'des': st.des}
        subjectType_dicts.append(subjectType_dic)
        count += 1
    res = {
        'code': 0,
        'msg': 'success',
        'count': count,
        'data': subjectType_dicts
    }
    return JsonResponse(res, safe=False)


# 获取账户种类数据
def getSubjectCategory(request):
    subjectCategoryList = models.SubjectCategory.objects.all()
    subjectCategory_dicts = []
    count = 0
    for sc in subjectCategoryList:
        subjectCategory_dic = {'id': sc.id, 'des': sc.des}
        subjectCategory_dicts.append(subjectCategory_dic)
        count += 1
    res = {
        'code': 0,
        'msg': 'success',
        'count': count,
        'data': subjectCategory_dicts
    }
    return JsonResponse(res, safe=False)


# 获取科目结构数据，可传递任意参数
def getSubjects(request):
    requestArgs = request.GET.dict()  # 获取参数字典
    qs = models.Subjects.objects  # 定义models查询对象
    qq = Q()  # 定义一个Q对象用来放入查询条件
    datalist = []  # 最终返回的数据列表
    count = 0  # 最终返回的数据数量
    subjectsList = []  # 定义查询结果列表
    if len(requestArgs) > 0:
        qq = reduce(operator.and_, [Q(**{k: requestArgs[k]}) for k in requestArgs])  # 如果接收到了参数，组装成查询条件对象
        subjectsList = qs.filter(qq)  # 执行查询过滤
    else:
        subjectsList = qs.all()  # 如果没有传递参数，则查询出所有数据
    for sub in subjectsList:
        if sub.level is None:
            level = ''
        else:
            level = sub.level
        if sub.category is None:
            category_id = ''
        else:
            category_id = sub.category.id
        sub_dic = {'subtype': sub.subtype.id, 'subcode': sub.subcode, 'subdescription': sub.subdescription,
                   'substatus': sub.substatus, 'needsummary': sub.needsummary, 'level': level,
                   'category': category_id}
        datalist.append(sub_dic)
        count += 1
    res = {
        'code': 0,
        'msg': 'success',
        'count': count,
        'data': datalist

    }
    return JsonResponse(res, safe=False)


# 获取下级科目数据
def getChildSubjects(request):
    subtype = request.GET.get('subtype')
    parent = request.GET.get('parent')
    code = 0
    msg = ''
    count = 0
    datalist = []
    if (subtype is None) | (parent is None):
        code = -1
        msg = '缺少科目类别参数subtype或者上级科目code参数parent'
    else:
        qs = models.Subjects.objects  # 定义models查询对象
        qq = Q(subtype=subtype)  # 定义一个Q对象用来放入查询条件
        subjectsList = qs.filter(Q(subtype=subtype), Q(subcode__startswith=parent))  # 定义查询结果列表
        for sub in subjectsList:
            sub_dic = {'subcode': sub.subcode, 'subdescription': sub.subdescription}
            datalist.append(sub_dic)
            count += 1
        code = 0
        msg = 'success'
    res = {
        'code': code,
        'msg': msg,
        'count': count,
        'data': datalist

    }
    return JsonResponse(res, safe=False)


# 新增账目接口
def addAcount(request):
    code = 0
    msg = 'success'
    requestArgs = request.POST.dict()  # 获取参数字典
    accountDetailcounts = 0
    for arg in requestArgs:
        if (str(arg).startswith('account-add-abstract')) and (requestArgs[arg] != ''):
            accountDetailcounts += 1
    if accountDetailcounts == 0:
        code = -1
        msg = '请添加账目明细后再提交！'
    else:
        recordtime = requestArgs['account-add-recordtime']
        vno = requestArgs['account-add-voucherno']
        debittotal = requestArgs['debittotal']
        credittotal = requestArgs['credittotal']
        biller = requestArgs['account-add-operatername']
        voucherfile = requestArgs['file']
        accountDetailList = []
        try:
            acb = models.AccountBaseInfo.objects.get_or_create(
                                                                recordtime=recordtime,
                                                                voucherno=vno,
                                                                debittotal=debittotal,
                                                                credittotal=credittotal,
                                                                biller=biller,
                                                                voucherfile=voucherfile
                                                               )
        except Exception as e:
            code = -1
            msg = str('acb.save:' + str(e))
        for i in range(1, accountDetailcounts+1):
            pcode = models.AccountBaseInfo.objects.filter(voucherno=vno).first()
            abstract = requestArgs['account-add-abstract-' + str(i)]
            subcodeset = requestArgs['account-add-account-'+str(i)]
            deamountstr = requestArgs['account-add-debitamount-'+str(i)]
            if deamountstr == '':
                deamount = 0
            else:
                deamountlist = deamountstr.split(',')
                deamount = float(''.join(deamountlist))
            cramountstr = requestArgs['account-add-creditamount-' + str(i)]
            if cramountstr == '':
                cramount = 0
            else:
                cramountlist = cramountstr.split(',')
                cramount = float(''.join(cramountlist))
            # 因为搜索的多组合性，这里还是将subcodeset拆分存储，后续将表中subcodeset字段拿掉
            subcodesetList = subcodeset.split(".")
            accdetail = AccountDetail(voucherno=pcode, abstract=abstract, subcodeset=subcodeset, fsubcode=subcodesetList[0]
                                      , ssubcode=subcodesetList[1], csubcode=subcodesetList[2],
                                      dsubcode=subcodesetList[3], debitamount=deamount, creditamount=cramount)
            accountDetailList.append(accdetail)
        try:
            acd = models.AccountDetail.objects.bulk_create(accountDetailList)
        except Exception as e:
            ado = models.AccountDetail.objects.filter(voucherno__voucherno=vno)
            if ado is not None:
                ado.delete()
            abo = models.AccountBaseInfo.objects.filter(voucherno=vno)
            if abo is not None:
                abo.delete()
            code = -1
            msg = str('acd.save:' + str(e))
    res = {
        'code': code,
        'msg': msg,
        'count': 0,
        'data': []

    }
    return JsonResponse(res, safe=False)

# 编辑账目调用的查询接口
def getAccountByParameter(request):
    code = 0
    msg = 'success'
    count = 0
    data_dict = {}

    voucherno = request.GET.get('voucherno')
    accountbase = models.AccountBaseInfo.objects.get(voucherno=voucherno)
    accountdetaillist = models.AccountDetail.objects.filter(voucherno=accountbase)
    ad_dicts = []
    for ad in accountdetaillist:
        subcodeset = ad.subcodeset
        subcodelist = subcodeset.split('.')
        subqs = models.Subjects.objects
        try:
            firstsub = subqs.get(subcode=subcodelist[0]).subdescription
        except models.Subjects.DoesNotExist:
            firstsub = '*'
        try:
            secondsub = subqs.get(subcode=subcodelist[1]).subdescription
        except models.Subjects.DoesNotExist:
            secondsub = '*'
        try:
            detailsub = subqs.get(subcode=subcodelist[2]).subdescription
        except models.Subjects.DoesNotExist:
            detailsub = '*'
        try:
            cashsub = subqs.get(subcode=subcodelist[3]).subdescription
        except models.Subjects.DoesNotExist:
            cashsub = '*'
        subtitle = ".".join([firstsub, secondsub, detailsub, cashsub])

        debitamount = ad.debitamount
        if debitamount == 0.00:
            debitamount = ''
        creditamount = ad.creditamount
        if creditamount == 0.00:
            creditamount = ''
        ad_dict = {"abstract": ad.abstract, "subcodeset":subcodeset, "subtitle": subtitle,
                   "debitamount": debitamount, "creditamount": creditamount}
        ad_dicts.append(ad_dict)
    data_dict = {
        "voucherno": accountbase.voucherno,
        "recordtime": accountbase.recordtime,
        "biller": accountbase.biller,
        "debittotal": accountbase.debittotal,
        "credittotal": accountbase.credittotal,
        "voucherfile": str(accountbase.voucherfile),
        "details": ad_dicts
    }
    res = {'code': code, 'msg': msg, 'count': count, 'data': data_dict}
    return JsonResponse(res, safe=False)

# 获取账目接口
def getAccounts(request):
    code = 0
    count = 0
    debittotalsum = 0
    credittotalsum = 0
    msg = 'success'
    datalist = []
    res = {'code': code, 'msg': msg, 'count': count, 'data': datalist, 'debittotalsum': debittotalsum, 'credittotalsum': credittotalsum}
    aBaseInfoQS = models.AccountBaseInfo.objects
    aDetailQS = models.AccountDetail.objects
    requestArgs = request.GET.dict()  # 获取参数字典
    # page=1&limit=10&voucherno=&daterange=&subject_1=&subject_2=&subject_detail=&subject_cash=
    del requestArgs["page"]
    del requestArgs["limit"]
    dq = {}
    aBaseInfoList = aBaseInfoQS.all()  # 初始化查询结果为所有数据
    for arg in list(requestArgs.keys()):
        if requestArgs[arg] == '':
            del requestArgs[arg]
        elif arg == "voucherno":
            aBaseInfoList = aBaseInfoQS.filter(voucherno=requestArgs[arg]) & aBaseInfoList  # 将凭证查询结果与所有结果取交集
        elif arg == "daterange":
            pass  # 时间区间搜索等下再写
        else:
            dq[arg] = requestArgs[arg]
    detailItems = aDetailQS.filter(**dq)
    if len(detailItems) != 0:
        vnolist = []
        for i in range(0, len(detailItems)):
            vnolist.append(detailItems[i].voucherno.voucherno)
        vnolist = list(set(vnolist))
    if len(vnolist) != 0:
        adBaseInfoList = aBaseInfoQS.filter(voucherno=vnolist[0])
        for i in range(1, len(vnolist)):
            adBaseInfoList = aBaseInfoQS.filter(voucherno=vnolist[i]) | adBaseInfoList
    aBaseInfoList = aBaseInfoList & adBaseInfoList
    # qq = Q()
    # if len(bq) > 0:
    #     qq = reduce(operator.or_, [Q(**{bq[k]: k}) for k in bq])  # 如果接收到了参数，组装成查询条件对象
    #     print("*********************", bq)
    #     # (AND: ('voucherno', '111111'), ('subject_1', '1001'), ('subject_2', '*'), ('subject_cash', '00'))
    #     aBaseInfoList = aBaseInfoQS.filter(qq)  # 执行查询过滤
    # else:
    #     aBaseInfoList = aBaseInfoQS.all()  # 如果没有传递参数，则查询出所有数据

    if len(aBaseInfoList) == 0:
        code = -1
        msg = '没有有效的数据'
        res['code'] = code
        res['msg'] = msg
        return JsonResponse(res, safe=False)
    for ab in aBaseInfoList:
        aDetailList = aDetailQS.filter(voucherno=ab)
        debittotalsum += ab.debittotal
        credittotalsum += ab.credittotal
        for ad in aDetailList:
            addebitamount = ad.debitamount
            if addebitamount == 0:
                addebitamount = ''
            else:
                addebitamount = "{:,}".format(addebitamount)
            adcreditamount = ad.creditamount
            if adcreditamount == 0:
                adcreditamount = ''
            else:
                adcreditamount = "{:,}".format(adcreditamount)
            debittotal = ab.debittotal
            if debittotal == 0:
                debittotal = ''
            else:
                debittotal = "{:,}".format(debittotal)
            credittotal = ab.credittotal
            if credittotal == 0:
                credittotal = ''
            else:
                credittotal = "{:,}".format(credittotal)
            subcodeset = ad.subcodeset
            subcodelist = subcodeset.split('.')
            subqs = models.Subjects.objects
            try:
                firstsub = subqs.get(subcode=subcodelist[0]).subdescription
            except models.Subjects.DoesNotExist:
                firstsub = '*'
            try:
                secondsub = subqs.get(subcode=subcodelist[1]).subdescription
            except models.Subjects.DoesNotExist:
                secondsub = '*'
            try:
                detailsub = subqs.get(subcode=subcodelist[2]).subdescription
            except models.Subjects.DoesNotExist:
                detailsub = '*'
            try:
                cashsub = subqs.get(subcode=subcodelist[3]).subdescription
            except models.Subjects.DoesNotExist:
                cashsub = '*'
            subtitle = ".".join([firstsub, secondsub, detailsub, cashsub])
            data_dict = {'abstract': ad.abstract,
                         'subcodeset': subcodeset,
                         'subtitle': subtitle,
                         'debitamount': addebitamount,
                         'creditamount': adcreditamount,
                         'voucherno': ab.voucherno,
                         'debittotal': debittotal,
                         'credittotal': credittotal,
                         'recordtime': ab.recordtime,
                         'biller': ab.biller,
                         'voucherfile': str(ab.voucherfile),
                         'billtime': ab.billtime,
                         'updatetime': ab.updatetime
                         }
            datalist.append(data_dict)
            count += 1
    res['code'] = code
    res['msg'] = msg
    res['count'] = count
    res['data'] = datalist
    res['debittotalsum'] = "{:,}".format(debittotalsum)
    res['credittotalsum'] = "{:,}".format(credittotalsum)
    return JsonResponse(res, safe=False)


# ---------------------------------以上------------------------------------#
# 获取一级科目及下面所有二级科目数据（旧）
def subjects(request):
    fsublist = models.FirstSubjects.objects.all()
    datalist = []
    count = 0
    for fsub in fsublist:
        fsubcode = int(fsub.fsubcode)
        fsubname = str(fsub.fsubname)
        total = 0
        ssublist = models.SecondSubjects.objects.filter(fathercode=fsub)
        ssub_dicts = []
        for ssub in ssublist:
            ssubcode = int(ssub.ssubcode)
            ssubname = str(ssub.ssubname)
            fathercode = fsubcode
            fathername = fsubname
            ssub_dict = {"ssubcode": ssubcode, "ssubname": ssubname, "fathercode": fathercode, "fathername": fathername}
            ssub_dicts.append(ssub_dict)
            total += 1
        fsub_dict = {
            "fsubcode": fsubcode, "fsubname": fsubname, "count": total, "cdata": ssub_dicts
        }
        datalist.append(fsub_dict)
        count += 1
    res = {
        'code': 0,
        'msg': 'success',
        'count': count,
        'data': datalist

    }
    return JsonResponse(res, safe=False)


# 获取明细段数据（旧）
def getDetailSubjects(request):
    dsublist = models.DetailSubjects.objects.all()
    dsub_dicts = []
    count = 0
    for dsub in dsublist:
        dsub_dic = {'dsubcode': dsub.dsubcode, 'dsubname': dsub.dsubname}
        dsub_dicts.append(dsub_dic)
        count += 1
    res = {
        'code': 0,
        'msg': 'success',
        'count': count,
        'data': dsub_dicts

    }
    return JsonResponse(res, safe=False)


# 获取现金段数据（旧）
def getCashSubjects(request):
    csublist = models.CashSubjects.objects.all()
    csub_dicts = []
    count = 0
    for csub in csublist:
        csub_dic = {'csubcode': csub.csubcode, 'csubname': csub.csubname}
        csub_dicts.append(csub_dic)
        count += 1
    res = {
        'code': 0,
        'msg': 'success',
        'count': count,
        'data': csub_dicts

    }
    return JsonResponse(res, safe=False)


# 返回科目数据表页面（旧）
def subjects(request):
    return render(request, 'subjects.html', locals())


def addSubject(request):
    """
    :param request:
    :return:
    """
    subtype = request.POST.get('subtype')
    code = request.POST.get('subject-add-code')
    name = request.POST.get('subject-add-name')
    psubcode = request.POST.get('subject-add-psubcode')
    file = request.POST.get('file')
    res = {
        'code': 0,
        'msg': 'success',
        'count': 0,
        'data': {}

    }
    return JsonResponse(res, safe=False)


# 获取全部账目数据
def get_accounts(request):
    accounts_list = models.AccountingVouchers.objects.all()
    accounts_dicts = []
    count = 0
    for acc in accounts_list:
        accounts_dic = {'recordtime': acc.recordtime, 'billtime': acc.billtime, 'updatetime': acc.updatetime,
                        'voucherno': acc.voucherno, 'abstract': str(acc.abstract), 'debitamount': acc.debitamount,
                        'debitfsubcode': str(acc.debitfsubcode), 'debitssubcode': str(acc.debitssubcode),
                        'debitdsubcode': str(acc.debitdsubcode), 'creditamount': acc.creditamount,
                        'creditfsubcode': str(acc.creditfsubcode), 'creditssubcode': str(acc.creditssubcode),
                        'creditdsubcode': str(acc.creditdsubcode),
                        'operatername': acc.operatername, 'voucherfile': str(acc.voucherfile)}
        accounts_dicts.append(accounts_dic)
        count += 1
    res = {
        'code': 0,
        'msg': 'success',
        'count': count,
        'data': accounts_dicts

    }
    return JsonResponse(res, safe=False)  # json.dumps(accounts_dict, cls=MyEncoder)


# 新增账目明细表格
def get_addaccountdetailtabletdlist(request):
    num = request.GET.get("num")
    if num is None:
        num = 5
        count = num
    addaccountdetailtabletdlist = []
    for i in range(1, num + 1):
        abstract_inputstr = '<input type="text" id="account-add-abstract-' + str(
            i) + '" name="account-add-abstract-' + str(i) + '" lay-verify="account-add-abstract" class="layui-input">'
        account_inputstr = '<input type="text" id="account-add-account-' + str(
            i) + '" name="account-add-account-' + str(i) + '" lay-verify="account-add-account" class="layui-input">'
        debitamount_inputstr = '<input type="text" id="account-add-debitamount-' + str(
            i) + '" name="account-add-debitamount-' + str(
            i) + '" lay-verify="account-add-debitamount" class="layui-input">'
        creditamount_inputstr = '<input type="text" id="account-add-creditamount-' + str(
            i) + '" name="account-add-creditamount-' + str(
            i) + '" lay-verify="account-add-creditamount" class="layui-input">'

        addaccountdetailtabletd = {'abstract_input': abstract_inputstr, 'account_input': account_inputstr,
                                   'debitamount_input': debitamount_inputstr,
                                   'creditamount_input': creditamount_inputstr}
        addaccountdetailtabletdlist.append(addaccountdetailtabletd)
    res = {
        'code': 0,
        'msg': 'success',
        'count': count,
        'data': addaccountdetailtabletdlist

    }
    return JsonResponse(res, safe=False)  # json.dumps(accounts_dict, cls=MyEncoder)


# 根据查询关键字获取单个账目
@csrf_exempt
def get_account(request):
    # return HttpResponse("12344")
    qk = request.GET.get('q')
    val = request.GET.get('v')
    if qk == "ssubcode":
        accList = models.AccountingVouchers.objects.filter(ssubcode=val)
    elif qk == "fsubcode":
        accList = models.AccountingVouchers.objects.filter(fsubcode=val)
    accounts_dict = []
    # for acc in accList:
    #     accounts_dic = {}
    #     accounts_dic['billtime'] = acc.billtime
    #     accounts_dic['updatetime'] = acc.updatetime
    #     accounts_dic['voucherno'] = acc.voucherno
    #     accounts_dic['abstract'] = acc.abstract
    #     accounts_dic['fsubcode'] = str(acc.fsubcode)
    #     accounts_dic['ssubcode'] = str(acc.ssubcode)
    #     accounts_dic['debitamount'] = acc.debitamount
    #     accounts_dic['creditamount'] = acc.creditamount
    #     accounts_dic['operatername'] = acc.operatername
    #     accounts_dic['voucherfile'] = str(acc.voucherfile)
    #     accounts_dict.append(accounts_dic)
    return JsonResponse(accounts_dict, safe=False)


# 新增账目
@csrf_exempt
def add_account(request):
    # billtime = request.POST.get('account-add-billtime')
    # voucherno = request.POST.get('account-add-voucherno')
    # abstract = request.POST.get('account-add-abstract')
    # fsubcode = request.POST.get('account-add-fsubcode')
    # ssubcode = request.POST.get('account-add-ssubcode')
    # debitamount = request.POST.get('account-add-debitamount')
    # creditamount = request.POST.get('account-add-creditamount')
    # operatertype = request.POST.get('account-add-operatertype')
    # operatername = request.POST.get('account-add-operatername')
    # voucherfile = request.POST.get('account-add-operatername')
    # acc = models.AccountingVouchers.objects.create(voucherno=voucherno, abstract=abstract, fsubcode=fsubcode, ssubcode=ssubcode,
    #                                        debitamount=debitamount, creditamount=creditamount, operatertype=operatertype,
    #                                        operatername=operatername, voucherfile=voucherfile)
    # acc.save()
    return JsonResponse({'message': 1}, safe=False)


# 编辑普通问题
@csrf_exempt
def edit_account(request):
    # voucherno = request.POST.get('voucherno')
    # abstract = request.POST.get('abstract')
    # fsubcode = request.POST.get('fsubcode')
    # ssubcode = request.POST.get('ssubcode')
    # debitamount = request.POST.get('debitamount')
    # creditamount = request.POST.get('creditamount')
    # operatertype = request.POST.get('operatertype')
    # operatername = request.POST.get('operatername')
    # voucherfile = request.POST.get('operatername')
    # acc = models.AccountingVouchers.get(voucherno=voucherno)
    # acc.voucherno=voucherno
    # acc.abstract = abstract
    # acc.fsubcode = fsubcode
    # acc.ssubcode = ssubcode
    # acc.debitamount = debitamount
    # acc.creditamount = creditamount
    # acc.debitamount = debitamount
    # acc.operatertype = operatertype
    # acc.operatername = operatername
    # acc.voucherfile = voucherfile
    # acc.save()
    return JsonResponse({'message': 1}, safe=False)


def index(request):
    return render(request, 'index.html', locals())


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        elif isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return super(MyEncoder, self).default(obj)


# 视图内被上传文件upload方法调用，导入一级科目到数据库
def addFirstSubjectsFromFile(fsubcode, fsubname):
    afs = models.FirstSubjects.objects.create(fsubcode=fsubcode, fsubname=fsubname)
    afs.save()


# 视图内被上传文件upload方法调用，导入二级科目到数据库
def addSecondSubjectsFromFile(ssubcode, ssubname, fathercode):
    qs = models.FirstSubjects.objects.filter(fsubcode=fathercode).first()
    fcode = qs
    ass = models.SecondSubjects.objects.create(ssubcode=ssubcode, ssubname=ssubname,
                                               fathercode=fcode)
    ass.save()


# 视图内被上传文件upload方法调用，导入明细段到数据库
def addDetailSubjectsFromFile(dsubcode, dsubname):
    ads = models.DetailSubjects.objects.create(dsubcode=dsubcode, dsubname=dsubname)
    ads.save()


# 视图内被上传文件upload方法调用，导入现金段到数据库
def addCashSubjectsFromFile(csubcode, csubname):
    acs = models.CashSubjects.objects.create(csubcode=csubcode, csubname=csubname)
    acs.save()


# 将excel数据写入mysql
def wrdb(fileurl):
    # 打开上传 excel 表格
    readboot = xlrd.open_workbook(fileurl)
    sheet = readboot.sheet_by_index(0)
    # 获取excel的行和列
    nrows = sheet.nrows
    ncols = sheet.ncols
    if sheet.cell_value(0, 0) == 'fsubcode':
        # sql = "insert into working_hours (jobnum,name,workingtime,category,project,date,createtime) VALUES"
        for i in range(1, nrows):
            try:
                addFirstSubjectsFromFile(int(sheet.row_values(i)[0]), str(sheet.row_values(i)[1]))
            except Exception as e:
                return e
    elif sheet.cell_value(0, 0) == 'ssubcode':
        for i in range(1, nrows):
            try:
                addSecondSubjectsFromFile(int(sheet.row_values(i)[0]), str(sheet.row_values(i)[1]),
                                          int(sheet.row_values(i)[2]))
            except Exception as e:
                return e
    elif sheet.cell_value(0, 0) == 'dsubcode':
        for i in range(1, nrows):
            try:
                addDetailSubjectsFromFile(int(sheet.row_values(i)[0]), str(sheet.row_values(i)[1]))
            except Exception as e:
                return e
    elif sheet.cell_value(0, 0) == 'csubcode':
        for i in range(1, nrows):
            try:
                addCashSubjectsFromFile(int(sheet.row_values(i)[0]), str(sheet.row_values(i)[1]))
            except Exception as e:
                return e
    return "success"


@csrf_exempt
def upload(request):
    # 根name取 file 的值
    file = request.FILES.get('file')
    print('uplaod:%s' % file)
    # 创建upload文件夹
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    url = r"upload\{time}".format(time=now_time)
    uploadurl = os.path.join(settings.BASE_DIR, url)
    code = 0
    msg = 'success'
    if not os.path.exists(uploadurl):
        os.makedirs(uploadurl)
    try:
        if file is None:
            return HttpResponse('请选择要上传的文件')
        # 循环二进制写入
        with open(uploadurl + "/" + file.name, 'wb') as f:
            for i in file.readlines():
                f.write(i)
        fileurl = uploadurl + "/" + file.name
        # 写入 mysql
        result = wrdb(fileurl)
        if result != 'success':
            code = -1
            msg = str(result)
    except Exception as e:
        code = -1
        msg = str(e)

    res = {
        'code': code,
        'msg': msg,
        'count': 0,
        'data': {}

    }
    return JsonResponse(res, safe=False)
