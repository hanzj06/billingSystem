
layui.config({
    version: '1610461958396' //为了更新 js 缓存，可忽略
});

layui.use(['laydate', 'laypage', 'layer', 'table', 'carousel', 'upload', 'element', 'form'], function(){
    var laydate = layui.laydate //日期
    ,laypage = layui.laypage //分页
    ,layer = layui.layer //弹层
    ,table = layui.table //表格
    ,carousel = layui.carousel //轮播
    ,upload = layui.upload //上传
    ,element = layui.element //元素操作
    ,form = layui.form //滑块
    ,$ = layui.$;

    //渲染新增账目界面 账目日期时间选择器
    laydate.render({
        elem: '#account-add-recordtime'
        ,calendar: true
        ,isInitValue: true
    });
    //渲染编辑账目界面 账目日期时间选择器
    laydate.render({
        elem: '#account-edit-recordtime'
        ,calendar: true
        ,isInitValue: true
    });

    //日期范围，账目表上方搜索-账目日期区间用
    laydate.render({
        elem: '#search-daterange-kw'
        ,range: true
    });

    //展示账目列表
    var accountsTable = table.render({
        elem: '#accounts'
        ,height: 'full-180'
        ,url: '/account/getAccounts/'   //数据接口
        ,title: '账目表'
        ,page: false //开启分页(后续实现)
        ,toolbar: '#toolbar' //开启工具栏，（后续自定义）#toolbar
        ,totalRow: true //开启合计行
        ,cols: [[ //表头
                    {field: 'voucherno', title: '凭证号', width:130}
                    ,{field: 'abstract', title: '摘要', width:250}
                    ,{field: 'subcodeset', title: '账户科目', width:350, templet:
                    '<div ><div title="{{d.subtitle}}" class="account-add-account">{{d.subcodeset}}</div></div>'}
                    ,{field: 'debitamount', title: '借方金额', width:120}
                    ,{field: 'creditamount', title: '贷方金额', width:120, totalRowText: '合计：'}
                    ,{field: 'debittotal', title: '借方总金额', width:120}
                    ,{field: 'credittotal', title: '贷方总金额', width:120}
                    ,{field: 'recordtime', title: '账目日期', width:120}
                    ,{field: 'biller', title: '入账人', width:80}
                    ,{field: 'voucherfile', title: '附件', width:120}
                    ,{field: 'billtime', title: '记账时间', width:120}
                    ,{field: 'updatetime', title: '修改时间', width:120}
                    ,{field: 'right', width: 165, align:'center', toolbar: '#barAccount'}
                ]]
        ,id: 'accountTableId'
        ,done: function (res, curr, count) {
                    $("td[data-field='voucherno']").find('div').attr("lay-event","account-voucherno"); //给数据div添加lay-event，以便监听debitamount
                    $("td[data-field='voucherno']").find('div').css('cursor','pointer');  //给数据div增加手型以示可点击
                    $("td[data-field='debitamount']").find('div').addClass('amount-value');
                    $("td[data-field='creditamount']").find('div').addClass('amount-value');
                    $("td[data-field='debittotal']").find('div').addClass('amount-value');
                    $("td[data-field='credittotal']").find('div').addClass('amount-value');
                    let debittotalsumobj = $("td[data-field='debittotal']")[$("td[data-field='debittotal']").length - 1];
                    $(debittotalsumobj).children('div').html(res.debittotalsum);
                    let credittotalsum = $("td[data-field='credittotal']")[$("td[data-field='credittotal']").length - 1];
                    $(credittotalsum).children('div').html(res.credittotalsum);
                    merge(res);
                }
    });

    // *******************数据单元格合并功能实现代码开始*****************************
    function merge(res) {
        //初始化分割点
        var indexPoint = [0];
        var data = res.data;
        var mergeIndex = 0;//定位需要添加合并属性的行数
        var mark = 1; //这里涉及到简单的运算，mark是计算每次需要合并的格子数
        //列名集合["orderNumber","reagentName","chineseVulgo","component","specifications","componentShelf","remarks"];
        /**
        * 执行第一列，已序号分组为准，产生分割点并保存
        */
        var $ = layui.$;
        var trArr = $(".layui-table-body>.layui-table").find("tr");//所有行
        for (var i = 1; i < res.data.length; i++) { //这里循环表格当前的数据
            var tdCurArr = trArr.eq(i).find("td").eq(0);//获取当前行的当前列
            var tdPreArr = trArr.eq(mergeIndex).find("td").eq(0);//获取相同列的第一列
            // console.log(k);
            if (data[i].voucherno === data[i - 1].voucherno) { //后一行的值与前一行的值做比较，相同就需要合并
                mark += 1;
                //相同列的第一列增加rowspan属性
                tdPreArr.each(function () {
                    $(this).attr("rowspan", mark);
                });
                //当前行隐藏
                tdCurArr.each(function () {
                    $(this).css("display", "none");
                });
            }else {
                //保存分割点
                indexPoint.push(i);
                mergeIndex = i;
                mark = 1;//一旦前后两行的值不一样了，那么需要合并的格子数mark就需要重新计算
            }
        }
        //补全最后一个分割点
        indexPoint.push(res.data.length);
        // console.log("合并索引点集合：",indexPoint)
        //依据拿到的分割点，对其他6列进行合并处理
        for(let i = 0;i<indexPoint.length;i++){
            let startIndex=0;
            if(i!==0){
                startIndex = indexPoint[i-1];
            }
            for(let j=startIndex;j<indexPoint[i];j++){
                //以第一列产生的区域分割点为基准，执行后面6列合并逻辑
                mergeSomeRows(5,startIndex,indexPoint[i],trArr,data,'voucherno');
                mergeSomeRows(6,startIndex,indexPoint[i],trArr,data,'debittotal');
                mergeSomeRows(7,startIndex,indexPoint[i],trArr,data,'credittotal');
                mergeSomeRows(8,startIndex,indexPoint[i],trArr,data,'recordtime');
                mergeSomeRows(9,startIndex,indexPoint[i],trArr,data,'biller');
                mergeSomeRows(10,startIndex,indexPoint[i],trArr,data,'voucherfile');
                mergeSomeRows(11,startIndex,indexPoint[i],trArr,data,'billtime');
                mergeSomeRows(12,startIndex,indexPoint[i],trArr,data,'updatetime');
                mergeSomeRows(13,startIndex,indexPoint[i],trArr,data,'12');
                mergeSomeRows(14,startIndex,indexPoint[i],trArr,data,'right');
            }
        }
    }
    /**
    *
    * @param colIndex:table中列索引
    * @param startIndex：合并单元格起始索引
    * @param endIndex：合并单元格结束索引
    * @param trArr：单列单元格元素集合
    * @param data：后端返回数据集合
    * @param colName：当前列字段名
    */
    function mergeSomeRows(colIndex,startIndex,endIndex,trArr,data,colName){
        var mark = 1;
        var $ = layui.$
        for(var j=startIndex+1;j<endIndex;j++){
            ++mark;
            var tdCurArr = trArr.eq(j).find("td").eq(colIndex);//获取当前行的当前列
            var tdPreArr = trArr.eq(startIndex).find("td").eq(colIndex);//获取相同列的第一列
            if (data[j][colName] === data[j - 1][colName]) { //后一行的值与前一行的值做比较，相同就需要合并
                //相同列的第一列增加rowspan属性
                tdPreArr.each(function () {
                    $(this).attr("rowspan", mark);
                });
                //当前行隐藏
                tdCurArr.each(function () {
                    $(this).css("display", "none");
                });
            }else {
                mark=1;
                startIndex=j;
            }
        }
    }
    // *******************数据单元格合并功能实现代码结束*****************************

    //监听头工具栏事件
    table.on('toolbar(accounts-table)', function(obj){
        var $ = layui.$;
        var checkStatus = table.checkStatus(obj.config.id)
        ,data = checkStatus.data; //获取选中的数据
        switch(obj.event){
            case 'add':
                layer.open({
                    type: 1
                    ,title: '新增账目'
                    ,area: ['90%', '660px']
                    ,shade: 0
                    ,maxmin: true
                    ,content: $('#account-add')
                    ,zIndex: layer.zIndex
                    ,success: function(layero){
                        layer.setTop(layero);
                    }
                    ,cancel:function () {
                        $('#account-add')[0].reset();
                        $('#account-select-title').text('*');
                    }
                });
                break;
            case 'refresh':
                table.reload('accountTableId');  //以当前筛选条件重载表格
                break;
        }
    });

    //定义重载
    var active = {
        reload: function(){
            var voucherno = $('#search-voucherno-kw').val();
            var daterange = $('#search-daterange-kw').val();
            var fsubcode = $('#search-subject-kw-1').val() != '*' ? $('#search-subject-kw-1').val():"";
            var ssubcode = $('#search-subject-kw-2').val() != '*' ? $('#search-subject-kw-2').val():"";
            var dsubcode = $('#search-subject-kw-detail').val() != '*' ? $('#search-subject-kw-detail').val():"";
            var csubcode = $('#search-subject-kw-cash').val() != '*' ? $('#search-subject-kw-cash').val():"";
            //执行重载
            table.reload('accountTableId', {
                where: {
                        voucherno: voucherno
                        ,daterange:daterange
                        ,fsubcode:fsubcode
                        ,ssubcode:ssubcode
                        ,csubcode:csubcode
                        ,dsubcode:dsubcode
                }
            }, 'data');
        }
    };

    //点击搜索重载表格
    $('.subTable .layui-btn').on('click', function(){
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });

    // 鼠标悬停事件
    $('.account-add-account').mouseover(function(e) {
        $('#account-select-title').text($(e.target).attr('title'));
    });

    $(document).on('mouseover','.account-add-account',function(e) {
        subcodesetobj = $("td[data-field='subcodeset']")[$("td[data-field='subcodeset']").length - 1];
        $(subcodesetobj).children('div').html(e.target.title);

    });
    // 选择账户，点击输入框弹出选择账户界面
    $('.account-add-account').on('focus',function (e) {
        var targetid = e.target.id;
        var targetvalue = e.target.value;
        if(targetvalue == ''){
            targetvalue = '*.*.*.*'
        }
        var selectvaluearr = targetvalue.split('.');
        layer.open({
            type: 1
            ,title: '选择账目账户'
            ,area: ['50%', '360px']
            ,shade: 0
            ,maxmin: true
            ,content: $('#subject-select')
            ,zIndex: layer.zIndex
            ,success: function(layero){
                layer.setTop(layero);
                $('#select-subject').attr('input-target',targetid);
                $('#account-add-fsubcode').val(selectvaluearr[0]);
                $('#account-add-ssubcode').val(selectvaluearr[1]);
                $('#account-add-detailsub').val(selectvaluearr[2]);
                $('#account-add-cashsub').val(selectvaluearr[3]);
                form.render('select');
            }
        });
        $(this).blur();
    });

    // 监听借方金额输入框失去焦点事件，失去后合计借方金额
    $('.account-add-debitamount').on('change',function (e) {
        var debittotal = 0;
        for (i=1; i<($('.account-add-debitamount').length + 1); i++){
            var debitamount = 0;
            var tdV = $('#account-add-debitamount-' + i).val();
            if(tdV == ''){
                tdV = '0';
            }
            var amountarr =  tdV.split(',');
            var amountV = parseFloat(amountarr.join(""));
            if(amountV == ''){
                debitamount = 0;
            }else{
                debitamount =  amountV;
            }
            debittotal = (debittotal*100 + debitamount*100)/100;
        }
        $('#totaldebit').html(format(debittotal));
    });
    // 监听贷方金额输入框失去焦点事件，失去后合计借方金额
    $('.account-add-creditamount').on('change',function (e) {
        var credittotal = 0;
        for (i=1; i<($('.account-add-creditamount').length + 1); i++){
            var creditamount = 0;
            var tdV = $('#account-add-creditamount-' + i).val();
            if(tdV == ''){
                tdV = '0';
            }
            var amountarr =  tdV.split(',');
            var amountV = parseFloat(amountarr.join(""));
            if(amountV == ''){
                creditamount = 0;
            }else{
                creditamount =  amountV;
            }
            credittotal = (credittotal*100 + creditamount*100)/100;
        }
        $('#totalcredit').html(format(credittotal));
    });
    //监听行工具事件
    table.on('tool(accounts-table)', function(obj){ //注：tool 是工具条事件名，test 是 table 原始容器的属性 lay-filter="对应的值"
        var data = obj.data //获得当前行数据
        ,layEvent = obj.event; //获得 lay-event 对应的值
        if(layEvent === 'del'){
            layer.confirm('真的删除行么', function(index){
                obj.del(); //删除对应行（tr）的DOM结构
                layer.close(index);
                //table.reload('accountTableId');
                //向服务端发送删除指令
            });
        } else if(layEvent === 'edit'){
            layer.msg('编辑操作');
        } else if(layEvent === 'account-voucherno'){
            $.get('/account/getAccountByParameter/?voucherno=' + obj.data.voucherno,function (data,status) {
                if(status == 'success'){
                    data = data.data
                    $('#account-edit-recordtime').attr('value', data.recordtime)
                    $('#account-edit-voucherno').attr('value', data.voucherno)
                    $('#account-edit-operatername').attr('value', data.biller)
                    // 预留附件展示

                    // 以下给详细账目表单添加数据
                    var insertStr = '';
                    for(i=1;i<data.details.length + 1;i++){
                        var debitamount = data.details[i-1].debitamount;
                        if(debitamount !=''){
                            var debitamount = format(parseFloat(debitamount));
                        }
                        var creditamount = data.details[i-1].creditamount;
                        if(creditamount !=''){
                            var creditamount = format(parseFloat(creditamount));
                        }
                        insertStr += '<tr><td class="edit-abstract-td">' +
                            '<input type="text" id="account-edit-abstract-'+ i +'" name="account-edit-abstract-'+ i +'" ' +
                                'lay-verify="account-edit-abstract" class="layui-input account-edit-abstract" autoinpu="false" onfocus="focusFun(this)" ' +
  'onclick="autoinput(this,\'edit\')" onblur="blurFun(this)" value='+ data.details[i-1].abstract +'><spam class="edit-abstract-clear" onclick="clearabstractinput(this,\'edit\')">X</spam></td>' +
  '<td><input type="text" id="account-edit-account-'+i+'" name="account-edit-account-'+i+'"  lay-verify="account-edit-account" ' +
  'class="layui-input account-eidt-account" onmouseover="mouseoverfun(this)" title='+ data.details[i-1].subtitle +' value='+ data.details[i-1].subcodeset +'></td><td><input type="text" id="account-edit-debitamount-'+i+'" ' +
  'name="account-edit-debitamount-'+i+'" autocomplete="off" lay-verify="account-edit-debitamount"' +
  'class="layui-input input-amount account-edit-debitamount" onkeyup="limit(this)" onblur="format(this)" value='+ debitamount +'></td><td>' +
  '<input type="text" id="account-edit-creditamount-'+i+'" name="account-edit-creditamount-'+i+'" autocomplete="off" ' +
  'lay-verify="account-edit-creditamount" class="layui-input input-amount account-edit-creditamount" ' +
  'onblur="format(this)" value='+ creditamount +'></td></tr>';
                    }
                    insertStr += '<tr class="layui-table-total input-amount"><td colspan="2" id="account-select-title-eidt">*</td><td id="totaldebit-edit">'+format(parseFloat(data.debittotal))+'</td><td id="totalcredit-edit">'+format(parseFloat(data.credittotal))+'</td></tr>'
                    $('#account-edit').find('tbody').html(insertStr);
                    layer.open({
                        type: 1
                        ,title: '编辑账目'
                        ,area: ['90%', '660px']
                        ,shade: 0
                        ,maxmin: true
                        ,content: $('#account-edit')
                        ,zIndex: layer.zIndex
                        ,success: function(layero){
                            $('#account-edit-voucherno').attr('disabled','disabled');
                            layer.setTop(layero);
                        }
                        ,cancel:function () {
                            $('#account-add')[0].reset();
                            $('#account-select-title').text('*');
                        }
                    });
                }
            });
        }
    });
    // 编辑界面，选择账户，点击输入框弹出选择账户界面
    $(document).on('click','.account-edit-account',function (e) {
        var targetid = e.target.id;
        var targetvalue = e.target.value;
        if(targetvalue == ''){
            targetvalue = '*.*.*.*'
        }
        var selectvaluearr = targetvalue.split('.');
        layer.open({
            type: 1
            ,title: '选择账目账户'
            ,area: ['50%', '360px']
            ,shade: 0
            ,maxmin: true
            ,content: $('#subject-select')
            ,zIndex: layer.zIndex
            ,success: function(layero){
                layer.setTop(layero);
                $('#select-subject').attr('input-target',targetid);
                $('#account-add-fsubcode').val(selectvaluearr[0]);
                $('#account-add-ssubcode').val(selectvaluearr[1]);
                $('#account-add-detailsub').val(selectvaluearr[2]);
                $('#account-add-cashsub').val(selectvaluearr[3]);
                form.render('select');
            }
        });
        $(this).blur();
    });
    //监听提交
    form.on('submit(add-account)', function(data){
        var debittotalarr =  $('#totaldebit').text().split(',');
        var debittotal = parseFloat(debittotalarr.join(""));
        data.field.debittotal = debittotal;
        var credittotalarr =  $('#totalcredit').text().split(',');
        var credittotal = parseFloat(credittotalarr.join(""));
        data.field.credittotal = credittotal;
        $.post('/account/addAcount/', data.field, function(data){
            console.log(data.code)
            if(data.code == 0){
               $('#account-add')[0].reset();
               layer.closeAll();
               layer.msg("添加成功！");
               table.reload('accountTableId');
               //table.render();
            }else {
                alert(2);
                layer.msg("添加失败！", );
                return false;
            }
        });
    });
    // 动态渲染账户各下拉选择框
    layer.ready(function () {
        $.get('/account/getSubjects/?subtype=1',function (data,status) {
            if(status === 'success'){
                var data = data.data;
                var op = '<option value="*"></option>';
                $.each(data,function(i,v){
                    op += '<option value="' + data[i].subcode + '">' + data[i].subdescription + '</option>';
                });
                $('#account-add-fsubcode').append(op);
                $('#search-subject-kw-1').append(op);
                form.render('select');
            }
        });
        $.get('/account/getSubjects/?subtype=4',function (data,status) {
            if(status === 'success'){
                var data = data.data;
                var op = '<option value="*"></option>';
                $.each(data,function(i,v){
                    op += '<option value="' + data[i].subcode + '">' + data[i].subdescription + '</option>';
                })
                $('#account-add-detailsub').append(op);
                 $('#search-subject-kw-detail').append(op);
                form.render('select');
            }
        });
        $.get('/account/getSubjects/?subtype=5',function (data,status) {
            if(status === 'success'){
                var data = data.data;
                var op = '<option value="*"></option>';
                $.each(data,function(i,v){
                    op += '<option value="' + data[i].subcode + '">' + data[i].subdescription + '</option>';
                })
                $('#account-add-cashsub').append(op);
                 $('#search-subject-kw-cash').append(op);
                form.render('select');
            }
        });
    });
    // 二级科目跟随一级科目选择进行相应更换
    form.on('select(account-add-fsubcode)',function (data) {
        $('#account-add-ssubcode').html('');
        $.get('/account/getChildSubjects/?subtype=2&parent=' + data.value,function (data,status) {
            if(status === 'success'){
                var data = data.data;
                var op = '<option value="*"></option>';
                $.each(data,function(i,v){
                    op += '<option value="' + data[i].subcode + '">' + data[i].subdescription + '</option>';
                });
                $('#account-add-ssubcode').append(op);
                form.render('select');
            }
        });
    });

    // 搜索区域  二级科目跟随一级科目选择进行相应更换
    form.on('select(search-subject-kw-1)',function (data) {
        $('#search-subject-kw-2').html('');
        $.get('/account/getChildSubjects/?subtype=2&parent=' + data.value,function (data,status) {
            if(status == 'success'){
                var data = data.data;
                var op = '<option value="*"></option>';
                $.each(data,function(i,v){
                    op += '<option value="' + data[i].subcode + '">' + data[i].subdescription + '</option>';
                });
                $('#search-subject-kw-2').append(op);
                form.render('select');
            }
        });
    });
    // 账户选择弹出框提交取消操作
    $('.select-subject-op').on('click',function (e) {
        if($(e.target).text() == '确定'){
            var inputid = $(e.target).attr('input-target');
            var fsubval = $('#account-add-fsubcode option:selected').val();
            var fsubtitle = $('#account-add-fsubcode option:selected').text();
            var ssubval = $('#account-add-ssubcode option:selected').val();
            var ssubtitle = $('#account-add-ssubcode option:selected').text();
            var dsubval = $('#account-add-detailsub option:selected').val();
            var dsubtitle = $('#account-add-detailsub option:selected').text();
            var csubval = $('#account-add-cashsub option:selected').val();
            var csubtitle = $('#account-add-cashsub option:selected').text();
            if( fsubval == undefined){
                fsubval = '*';
                fsubtitle = '*';
            }else if(fsubval == '*'){
                fsubtitle = '*';
            }
            if( ssubval == undefined){
                ssubval = '*';
                ssubtitle = '*';
            }else if(ssubval == '*'){
                ssubtitle = '*';
            }
            if( dsubval == undefined){
                dsubval = '*';
                dsubtitle = '*';
            }else if(dsubval == '*'){
                dsubtitle = '*';
            }
            if( csubval == undefined){
                csubval = '*';
                csubtitle = '*';
            }else if(csubval == '*'){
                csubtitle = '*';
            }
            var selectval = fsubval + '.' + ssubval + '.' + dsubval + '.' + csubval;

            var titleval = fsubtitle + '.' + ssubtitle + '.' + dsubtitle + '.' + csubtitle;

            if(selectval == '*.*.*.*'){
                selectval = '';
                titleval = '';
            }
            $('#' +inputid).val(selectval);
            $('#' +inputid).attr('title',titleval);
            $('#account-select-title').text(titleval);
        }
        $('#subject-select-form')[0].reset();
        form.render();
        layer.close(layer.index);
    });
    //分页
    laypage.render({
        elem: 'pageDemo' //分页容器的id
        ,count: 100 //总页数
        ,skin: '#1E9FFF' //自定义选中色值
        //,skip: true //开启跳页
        ,jump: function(obj, first){
            if(!first){
                layer.msg('第'+ obj.curr +'页', {offset: 'b'});
            }
        }
    });
    //上传
    upload.render({
        elem: '#account-add-voucherfile'
        ,url: '/account/test/' //改成您自己的上传接口
        ,accept:'file'
        ,done: function(res){
            layer.msg('上传成功');
            layui.$('#account-add-voucherfile-view').removeClass('layui-hide').find('xls').attr('src', res.files.file);
        }
    });
    //底部信息
    layer.ready(function(){
        var $ = layui.$;
        var footerTpl = '';
        $.get('https://v1.hitokoto.cn/',function(data, status){
            footerTpl = (data.hitokoto) + '————' + data.from;
            lay('#footer').html(layui.laytpl(footerTpl).render({})).removeClass('layui-hide');
        });
    });

    $("#account-tr-add-td").mouseover(function (){
        $("#account-tr-add-icon").show();
    }).mouseout(function (){
        $("#account-tr-add-icon").hide();
    });

     $("#account-tr-add-td").bind("click",function (e) {
        console.log(e);
     })
});
function format(arg) {
    var formatV;
    if(typeof (arg) == 'number'){
        formatV = arg.toString();
    }else if(typeof (arg) == 'object'){
        formatV = arg.value;
    }else{
        return;
    }
    var array = new Array();
    array = formatV.split(".");
    if (array.length == 1 && array[0].length>0){
        array[1] = '00';
    }else if(array.length == 2 && array[1].length<2){
        array[1] = array[1] + '0';
    }
    var re = /(-?\d+)(\d{3})/;
    while (re.test(array[0])) {
        array[0] = array[0].replace(re, "$1,$2")
    }
    var returnV = array[0];
    for (var i = 1; i < array.length; i++) {
        returnV += "." + array[i];
    }
    if(typeof (arg) == 'number'){
        return returnV;
    }else if(typeof (arg) == 'object'){
        arg.value = returnV;
    }else {
        return;
    }
}
function limit(element) {
    element.value = element.value.replace(/[^\d.]/g,"");
    element.value = element.value.replace(/^\./g,"");
    element.value = element.value.replace(".","$#$").replace(/\./g,"").replace("$#$",".");
    element.value = element.value.replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3');
}
function focusFun(element) {
    spamObj = $(element).parent().find('spam');
    spamObj.show();
}
function blurFun(element) {
    setTimeout(function() {
        spamObj = $(element).parent().find('spam');
        spamObj.hide();
    },300);
}
function mouseoverfun(element) {
    console.log($(element).attr('title'));
    $('#account-select-title-eidt').text($(element).attr('title'));
}
function autoinput(element,str) {
    if($(element).attr('autoinpu') == 'true'){
        if($(element).parent().parent().prev().length == 0){
            $(element).attr('autoinpu','false');
        }else if($(element).parent().parent().prev().length == 1){
            obj = $(element).parent().parent().prev();
            autovalue = $(obj).find('.account-' + str +'-abstract')[0].value;
            element.value = autovalue;
            $(element).attr('autoinpu','false')
        }
    }
}
function clearabstractinput(element,str) {
    inputObj = $(element).parent().find('.account-'+ str +'-abstract');
    inputObj.val('');
    $(element).hide()
}
