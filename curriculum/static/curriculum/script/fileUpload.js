'use strict';

function createOption(val, name) {
    var ret = document.createElement('option');
    ret.value = val;
    ret.textContent = name;
    return ret;
}

function startResourceUpload(file) {
    return new Promise(function(resolve, reject) {
        var formData = new FormData();
        formData.append('file', file, file.name);

        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function(ev) {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                var lessonResourceId = xhr.response['id'];
                if (lessonResourceId !== undefined) {
                    resolve(lessonResourceId);
                } else {
                    reject(xhr.response['err']);
                }
            }
        };

        // Requires that CSRF_TOKEN has been set. This is done in lessonplan_new.html.
        xhr.open('POST', '/lesson-resource/', true);
        xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
        xhr.responseType = 'json';
        xhr.send(formData);
    });
}

function addResourceForm(file, idPromise) {
    var formDiv = document.getElementById('lesson-resource-forms');

    var form = document.createElement('form');
    formDiv.appendChild(form);
    form.setAttribute('method', 'post');
    form.setAttribute('enctype', 'multipart/form-data');
    form.className = 'lesson-resource-form';

    var filenameInput = document.createElement('input');
    form.appendChild(filenameInput);

    filenameInput.className = 'six column';

    filenameInput.setAttribute('type', 'text');
    filenameInput.setAttribute('name', 'name');
    filenameInput.value = file.name;

    var typeInput = document.createElement('select');
    form.appendChild(typeInput);

    typeInput.className = 'four column';
    typeInput.required = true;

    typeInput.appendChild(createOption("", "---------"));
    typeInput.appendChild(createOption(1, "Student Handout"));
    typeInput.appendChild(createOption(2, "Teacher Reference"));
    typeInput.appendChild(createOption(3, "Slides"));
    typeInput.appendChild(createOption(4, "Code"));
    typeInput.appendChild(createOption(5, "Schematic"));
    typeInput.appendChild(createOption(0, "Other"));

    var removeIcon = document.createElement('i');
    form.appendChild(removeIcon);

    removeIcon.className = 'one column icon-remove';

    removeIcon.addEventListener('click', function (event) {
        idPromise.then(function (id) {
            var xhr = new XMLHttpRequest();

            xhr.onreadystatechange = function(event) {
                if(xhr.readyState === XMLHttpRequest.DONE) {
                    formDiv.removeChild(form);
                }
            };

            xhr.open('DELETE', '/lesson-resource/' + id + '/');
            xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
            xhr.send();
        });
    });
}

function submitLessonPlan(event) {
    event.preventDefault();

    var allowSubmission = true;

    var resources = document.getElementsByClassName('lesson-resource-form');
    for(var index = 0; index < resources.length; ++index) {
        // Figure out a way to merge this form data to send as one big whole,
        // or better yet do them separately, but in the background before
        // submitting the main lesson plan form.
        var resource = resources[index];
        allowSubmission = allowSubmission && resource.reportValidity();
    }

    var lessonPlanForm = document.getElementById('lesson-plan-form');
    allowSubmission = allowSubmission && lessonPlanForm.reportValidity();

    if(allowSubmission) {
        lessonPlanForm.submit();
    }
}

window.addEventListener('DOMContentLoaded', function(e) {
    var fileSelect = document.getElementById('file-select');
    fileSelect.addEventListener('change', function(event) {
        var files = fileSelect.files;
        for(var index = 0; index < files.length; ++index) {
            var idPromise = startResourceUpload(files[index]);
            idPromise.then(function(id) {
                console.log(id);
            });
            addResourceForm(files[index], idPromise);
        }
    });

    var submitLessonPlanBtn = document.getElementById('submit-lesson-plan');
    submitLessonPlanBtn.addEventListener('click', submitLessonPlan);
});
