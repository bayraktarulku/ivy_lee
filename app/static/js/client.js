var BASEURL = 'http://127.0.0.1:5000/api';
// var TOKEN = 'e1e6b7b6399aaed903c37e18654339e27e0e6abf';
function request(method, location, headers, data) {
    r = new XMLHttpRequest();
    r.open(method, location, false);
    for (var i = headers.length - 1; i >= 0; i--) {
        r.setRequestHeader(headers[i][0], headers[i][1]);
    }
    r.send(data);
    response = r.responseText;
    return response;
}

function getDayOfYear() {
    var now = new Date();
    var start = new Date(now.getFullYear(), 0, 0);
    var diff = now - start;
    var oneDay = 1000 * 60 * 60 * 24;
    var day = Math.floor(diff / oneDay);
    return day;
}

function getUserList(data) {
    data = JSON.stringify(data);
    token = sessionStorage.getItem('token')
    resp = request('POST', BASEURL + '/user', [['Content-Type', 'application/json'], ['X-Token', token]], data);
    data = JSON.parse(resp);
    return data;
}

function taskCheck(task_id, checked) {
    requestData = JSON.stringify({'id': task_id, 'checked': checked});
    token = sessionStorage.getItem('token')
    resp = request('PUT', BASEURL + '/task', [['Content-Type', 'application/json'],['X-Token', token]], requestData);
    data = JSON.parse(resp);
    return data;
}

function addTask(description) {
    day = getDayOfYear();
    data = JSON.stringify({'description': description, 'date_time': day});
    token = sessionStorage.getItem('token')
    resp = request('POST', BASEURL + '/task', [['Content-Type', 'application/json'],['X-Token', token]], data);
    return JSON.parse(resp);
}
