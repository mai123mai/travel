function MyupdateTable(evn, col_name) {
    var xmlhttp = new XMLHttpRequest();
    var json_rep;
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            // var json_rep = xmlhttp.responseText.parseJSON();
            json_rep = JSON.parse(xmlhttp.responseText)
        }
    }
    xmlhttp.open("GET", "http://127.0.0.1:8888/getAlarmMsg?evn=" + evn + "&col_name=" + col_name, false);
    xmlhttp.send();
    return json_rep;
}


// 将json数据转成obj数组
function transData(json_rep, dataTable) {
    len = json_rep['len']
    for (var i = 0; i < len; i++) {
        dataTable.push({
            id: json_rep['id'][i],
            sid: json_rep['sid'][i],
            title: json_rep['title'][i],
            detail_link: json_rep['detail_link'][i],
            main_img: json_rep['main_img'][i],
            address: json_rep['address'][i]
        })
    }
    return dataTable
}

var tke_room_nums_data = []
rep_tke_room_nums = MyupdateTable("tke", "room_nums")
tke_room_nums_data = transData(rep_tke_room_nums, tke_room_nums_data)

// 对于表单结构、模式进行设置
$('#table').bootstrapTable(
    {
        search: true,
        pagination: true,   //启动分页
        striped: true,    //设置为 true 会有隔行变色效果
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pageSize: 6,//初始页记录数
        sortable: true,    //排序
        pageList: [6, 36, 72, 144], //记录数可选列表
        smartDisplay: false,    //程序自动判断显示分页信息
        columns: [{
            field: 'id',
            title: 'ID'
        }, {
            field: 'sid',
            title: '时间'
        }, {
            field: 'title',
            title: '参数名'
        }, {
            field: 'detail_link',
            title: '实际值'
        },
            {
                field: 'main_img',
                title: '预测范围'
            },
            {
                field: 'address',
                title: '是否告警'
            },
        ],
        data: tke_room_nums_data
    }
)


//bootstrapTable数据表格回显
function doQuery() {
    var curPage = 1;
    var pageSize = 5;

    $('#table').bootstrapTable({
        url: '/getAlarmMsg_data',
        method: 'get',                      //请求方式（*）
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
        striped: true,                      //是否显示行间隔色
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pagination: true,                   //是否显示分页（*）
        sortable: true,                     //是否启用排序
        sortOrder: "asc",                   //排序方式
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
        strictSearch: false,
        pageSize: pageSize,
        showHeader: true,
        showColumns: false,                  //是否显示所有的列
        showRefresh: true,                  //是否显示刷新按钮
        minimumCountColumns: 2,             //最少允许的列数
        clickToSelect: true,                //是否启用点击选中行
        detailView: false,
        pageList: [5],
        onPageChange: function (number, size) {
            curPage = number; //第几页
            pageSize = size; // 每页显示条数
        },
        queryParams: getParams,//携带参数
        columns: [
            {
                field: 'id',
                title: 'ID'
            }, {
                field: 'sid',
                title: '时间'
            }, {
                field: 'title',
                title: '参数名'
            }, {
                field: 'detail_link',
                title: '实际值'
            },
            {
                field: 'main_img',
                title: '预测范围'
            },
            {
                field: 'address',
                title: '是否告警'
            },
        ],
    });

    function getParams(params) {
        var temp = {
            curPage: (params.offset / params.limit) + 1,
            pageSize: pageSize,
        }
        return temp;
    }

}

doQuery()


