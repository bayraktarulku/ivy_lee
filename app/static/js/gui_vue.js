var BASEURL = 'http://127.0.0.1:5000/api';
var TOKEN = 'e1e6b7b6399aaed903c37e18654339e27e0e6abf';


function async_request(method, location, headers, data, callback) {
  var r = new XMLHttpRequest();
  r.open(method, location);
  header_keys = Object.keys(headers);
  for (var i = header_keys.length - 1; i >= 0; i--) {
    r.setRequestHeader(header_keys[i], headers[header_keys[i]]);
  }
  r.onreadystatechange = function() {
    if (r.readyState == 4){
        callback(r.responseText);
    }
  };
  r.send(data);
}


function getDayOfYear() {
    var now = new Date();
    var start = new Date(now.getFullYear(), 0, 0);
    var diff = now - start;
    var oneDay = 1000 * 60 * 60 * 24;
    var day = Math.floor(diff / oneDay);
    return day;
}

Vue.component('task-list', {
  'props': ['task'],
  'template': '\
      <li v-bind:class="{done: task.checked}" v-on:click="taskCheck(task)">\
        <label for="checkbox">{{ task.description }}</label>\
        <button class="delete" v-on:click="removeTask(task)">X</button>\
      </li>',
  'methods':{
    'removeTask': function(task) {
      app.removeTask(task);
    },
    'taskCheck': function (task) {
      app.taskCheck(task);
    }
  }
});

Vue.component('tomorrow-task-list', {
  'props': ['task'],
  'template': '\
      <li v-bind:class="{done: task.checked}">\
        <label for="checkbox">{{ task.description }}</label>\
      </li>',
});

var app = new Vue({
  'el': "#todo",
  'data': {
    newTask: '',
    taskList: [],
    getTasks: [],
    tomorrorGetTasks: [],
    taskLimit: null,
  },
  'created': function() {
    this.getUserList();
  },
  'methods': {
    'getUserList': function() {
      data = {'username': 'ulku', 'password': 'ulku123'};
      data = JSON.stringify(data);
      token = sessionStorage.getItem('token');
      async_request('POST', BASEURL + '/user', {'Content-Type': 'application/json', 'X-Token': token}, data,
        this.getUserCallback);
    },
    'getUserCallback': function (response) {
      tasksData = JSON.parse(response).tasks;
      this.taskLimit = JSON.parse(response).limit;

      today = getDayOfYear();
      yesterday = today-1;

      for (var i = tasksData.length - 1; i >= 0; i--) {
        if (tasksData[i].date_time < yesterday && this.taskLimit >= this.getTasks.length) {
         this.getTasks.push(tasksData[i]);
        } else {
          this.tomorrorGetTasks.push(tasksData[i]);
        }
      }

    },
    'addTask': function() {
        day = getDayOfYear();
        data = JSON.stringify({'description': this.newTask, 'date_time': day});
        token = sessionStorage.getItem('token')
        if (this.newTask != '' & this.taskLimit >= this.getTasks.length) {
          async_request('POST', BASEURL + '/task', {'Content-Type': 'application/json', 'X-Token': token}, data,
            this.addTaskCallback);
        }
    },
    'addTaskCallback': function(response) {
      newTaskData = JSON.parse(response);
      if (this.taskLimit >= this.getTasks.length) {
        this.getTasks.push(newTaskData);
      } else {
        this.tomorrorGetTasks.push(newTaskData);
      }
      this.newTask = '';
    },
    'removeTaskCallback': function (response) {
      data = JSON.parse(response);
      return data;
    },
    'removeTask': function(task) {
      var index = this.getTasks.indexOf(task);
      this.getTasks.splice(index, 1);
      data = JSON.stringify({'id': task.id});
      token = sessionStorage.getItem('token');
      async_request('DELETE', BASEURL + '/task', {'Content-Type': 'application/json', 'X-Token': token}, data,
        this.removeTaskCallback);
    },

    clearList: function() {
      this.getTasks = [];
    },
    'taskCheckCallBack': function (response) {
      data = JSON.parse(response);
    },
    'taskCheck': function (task) {
      task.checked = true;
      data = JSON.stringify({'id': task.id, 'checked': true});
      token = sessionStorage.getItem('token')
      resp = async_request('PUT', BASEURL + '/task', {'Content-Type': 'application/json', 'X-Token': token}, data,
        this.taskCheckCallBack);
    }
  }
});
