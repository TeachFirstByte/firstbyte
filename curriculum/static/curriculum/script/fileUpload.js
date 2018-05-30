'use strict';

function createOption(num, name) {
    var ret = document.createElement('option');
    ret.setAttribute('value', num);
    ret.textContent = name;
    return ret;
}

function add_resource_form(file) {
    var formDiv = document.getElementById('lesson-resource-forms');

    var form = document.createElement('form');
    formDiv.appendChild(form);
    form.setAttribute('method', 'post');
    form.setAttribute('enctype', 'multipart/form-data');
    form.className = 'lesson-resource-form';

    var filenameInput = document.createElement('input');
    form.appendChild(filenameInput);
    filenameInput.setAttribute('type', 'text');
    filenameInput.setAttribute('name', 'name');
    filenameInput.value = file.name;

    var typeInput = document.createElement('select');
    form.appendChild(typeInput);

    typeInput.appendChild(createOption(0, "Student Handout"));
    typeInput.appendChild(createOption(1, "Teacher Reference"));
    typeInput.appendChild(createOption(2, "Slides"));
    typeInput.appendChild(createOption(3, "Code"));
    typeInput.appendChild(createOption(4, "Schematic"));
}

window.addEventListener('DOMContentLoaded', function(e) {
    var fileSelect = document.getElementById('file-select');
    fileSelect.addEventListener('change', function(event) {
        var files = fileSelect.files;
        for(var index = 0; index < files.length; ++index) {
            add_resource_form(files[index]);
        }
    });
});
