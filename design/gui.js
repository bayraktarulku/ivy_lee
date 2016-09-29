function checkbox_toggle(element) {
    element.classList.toggle('fa-square-o');
    element.classList.toggle('fa-check-square-o');
}

function createListItem(description) {
    d = document.createElement('div');
    d.classList.add('task');
    c = document.createElement('i');
    c.className = 'fa fa-lg fa-square-o';
    c.setAttribute('onclick', 'checkbox_toggle(this);');
    f = document.createElement('font');
    f.innerHTML = description;
    d.appendChild(c);
    d.appendChild(f);
    return d;
}