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


// ��json����ת��obj����
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

// ���ڱ��ṹ��ģʽ��������
$('#table').bootstrapTable(
    {
        search: true,
        pagination: true,   //������ҳ
        striped: true,    //����Ϊ true ���и��б�ɫЧ��
        cache: false,                       //�Ƿ�ʹ�û��棬Ĭ��Ϊtrue������һ���������Ҫ����һ��������ԣ�*��
        pageSize: 6,//��ʼҳ��¼��
        sortable: true,    //����
        pageList: [6, 36, 72, 144], //��¼����ѡ�б�
        smartDisplay: false,    //�����Զ��ж���ʾ��ҳ��Ϣ
        columns: [{
            field: 'id',
            title: 'ID'
        }, {
            field: 'sid',
            title: 'ʱ��'
        }, {
            field: 'title',
            title: '������'
        }, {
            field: 'detail_link',
            title: 'ʵ��ֵ'
        },
            {
                field: 'main_img',
                title: 'Ԥ�ⷶΧ'
            },
            {
                field: 'address',
                title: '�Ƿ�澯'
            },
        ],
        data: tke_room_nums_data
    }
)


//bootstrapTable���ݱ�����
function doQuery() {
    var curPage = 1;
    var pageSize = 5;

    $('#table').bootstrapTable({
        url: '/getAlarmMsg_data',
        method: 'get',                      //����ʽ��*��
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
        striped: true,                      //�Ƿ���ʾ�м��ɫ
        cache: false,                       //�Ƿ�ʹ�û��棬Ĭ��Ϊtrue������һ���������Ҫ����һ��������ԣ�*��
        pagination: true,                   //�Ƿ���ʾ��ҳ��*��
        sortable: true,                     //�Ƿ���������
        sortOrder: "asc",                   //����ʽ
        sidePagination: "server",           //��ҳ��ʽ��client�ͻ��˷�ҳ��server����˷�ҳ��*��
        search: false,                       //�Ƿ���ʾ����������������ǿͻ������������������ˣ����ԣ����˸о����岻��
        strictSearch: false,
        pageSize: pageSize,
        showHeader: true,
        showColumns: false,                  //�Ƿ���ʾ���е���
        showRefresh: true,                  //�Ƿ���ʾˢ�°�ť
        minimumCountColumns: 2,             //�������������
        clickToSelect: true,                //�Ƿ����õ��ѡ����
        detailView: false,
        pageList: [5],
        onPageChange: function (number, size) {
            curPage = number; //�ڼ�ҳ
            pageSize = size; // ÿҳ��ʾ����
        },
        queryParams: getParams,//Я������
        columns: [
            {
                field: 'id',
                title: 'ID'
            }, {
                field: 'sid',
                title: 'ʱ��'
            }, {
                field: 'title',
                title: '������'
            }, {
                field: 'detail_link',
                title: 'ʵ��ֵ'
            },
            {
                field: 'main_img',
                title: 'Ԥ�ⷶΧ'
            },
            {
                field: 'address',
                title: '�Ƿ�澯'
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


