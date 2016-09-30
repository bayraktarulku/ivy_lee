// var BASEURL = '/api';
data = {'username': 'ulku', 'password': 'ulku123'};

function createTaskContainer() {
    c = document.createElement('div');
    toDo = document.createElement('div');
    toDo.className = 'to-do';
    c.appendChild(toDo);
    nextToDo = document.createElement('div');
    nextToDo.className = 'next-to-do';
    c.appendChild(nextToDo);
    c.style = 'height:100%';
    return c;
}

function checkbox_toggle(element) {
    if(element.classList.contains('fa-check-square-o')) {
        element.classList.remove('fa-check-square-o');
        element.classList.add('fa-square-o');
        element.nextSibling.classList.add('task-done-text');
    } else {
        element.classList.remove('fa-square-o');
        element.classList.add('fa-check-square-o');
        element.nextSibling.classList.remove('task-done-text');
    }
}

function createTodaysTask(task) {
    d = document.createElement('div');
    d.classList.add('todays-task');
    c = document.createElement('i');
    c.className = 'fa fa-lg fa-square-o';
    c.setAttribute('onclick', 'checkbox_toggle(this);');
    console.log(task.checked);
    f = document.createElement('font');
    f.innerHTML = task.description;
    d.appendChild(c);
    d.appendChild(f);
    if(task.checked) {
        c.onclick();
    }
    return d;
}

function createTomorrowsTask(task) {
    d = document.createElement('div');
    d.classList.add('tomorrows-task');
    f = document.createElement('font');
    f.innerHTML = task.description;
    d.appendChild(f);
    return d;
}

function getDayOfYear() {
    var now = new Date();
    var start = new Date(now.getFullYear(), 0, 0);
    var diff = now - start;
    var oneDay = 1000 * 60 * 60 * 24;
    var day = Math.floor(diff / oneDay);
    return day;
}

function fillUserTasks(container, data) {
    tasksData = getUserList(data).tasks;
    for (var i = tasksData.length - 1; i >= 0; i--) {
        console.log(tasksData[i]);
        today = getDayOfYear();
        if(tasksData[i].date_time < today) {
            t = createTodaysTask(tasksData[i]);
            container.children[0].appendChild(t);
        } else {
            t = createTomorrowsTask(tasksData[i]);
            container.children[1].appendChild(t);
        }
    }
}