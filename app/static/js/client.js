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

function getUserList(data) {
    data = JSON.stringify(data);
    resp = request('POST', 'http://127.0.0.1:5000/api/user', [['Content-Type', 'application/json']], data);
    data = JSON.parse(resp);
    return data;
}
