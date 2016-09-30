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
        resp = taskCheck(element.parentElement.task_id, false);
        element.classList.remove('fa-check-square-o');
        element.classList.add('fa-square-o');
        element.nextSibling.classList.remove('task-done-text');
    } else {
        resp = taskCheck(element.parentElement.task_id, true);
        element.classList.remove('fa-square-o');
        element.classList.add('fa-check-square-o');
        element.nextSibling.classList.add('task-done-text');
    }
}

function createTodaysTask(task) {
    d = document.createElement('div');
    d.classList.add('todays-task');
    c = document.createElement('i');
    c.className = 'fa fa-lg';
    c.setAttribute('onclick', 'checkbox_toggle(this);');
    f = document.createElement('font');
    f.innerHTML = task.description;
    d.appendChild(c);
    d.appendChild(f);
    if(task.checked) {
        c.classList.add('fa-check-square-o');
        f.classList.add('task-done-text');
    } else {
        c.classList.add('fa-square-o');
        f.classList.remove('task-done-text');
    }
    d.task_id = task.id;
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

function addTaskOnclick(element) {
    description = element.nextSibling.value;
    resp = addTask(description);
    if(resp.status == 'OK') {
        t = createTomorrowsTask(resp);
        element.parentElement.parentElement.insertBefore(t, element.parentElement);
        element.nextSibling.value = '';
    }
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
    addButton = document.createElement('button');
    addButton.classList.add('task-adding-button');
    i = document.createElement('i');
    i.className = 'fa fa-lg fa-plus';
    f = document.createElement('font');
    f.innerHTML = 'Add Task';
    addTaskInput = document.createElement('input');
    addTaskInput.className = 'task-adding-input';
    addButton.setAttribute('onclick', 'addTaskOnclick(this);');
    addButton.appendChild(i);
    addButton.appendChild(f);
    d = document.createElement('div');
    d.className = 'task-adding-container';
    d.appendChild(addButton);
    d.appendChild(addTaskInput);
    container.children[1].appendChild(d);
}