var BASEURL = 'http://127.0.0.1:5000/api';

var app = new Vue({
  'el': '#login-app',
  'data': {
      'username': '',
      'password': ''
  },
  'methods': {
    'login_submit': function () {
        data = JSON.stringify({'username': this.username, 'password': this.password});
        r = new XMLHttpRequest();
        r.open('POST', BASEURL + '/auth', false);
        r.setRequestHeader('Content-Type', 'application/json');
        r.send(data);
        if (r.status == 200) {
            response = JSON.parse(r.responseText);
            sessionStorage.setItem('token', response.token);
            window.location = '/task';
        } else {
            alert('Wrong Username or Password ');
        }
      }
    }
});
