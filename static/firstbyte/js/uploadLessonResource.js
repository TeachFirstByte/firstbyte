'use strict';

import $ from 'jquery';
import Promise from 'bluebird';

import { CurriculumClient } from './restClient.js';

function _createOption(val, name) {
    var ret = document.createElement('option');
    ret.value = val;
    ret.textContent = name;
    return ret;
}

function ResourceForm(filename, onRemove) {
    this.onRemove = onRemove || (function(_) { return Promise.resolve(true); });

    var form = document.createElement('form');
    form.className = 'lesson-resource-form';
    form.setAttribute('method', 'post');
    form.setAttribute('enctype', 'multipart/form-data');

    var filenameInput = document.createElement('input');
    form.appendChild(filenameInput);
    filenameInput.className = 'six column';
    filenameInput.value = filename;
    filenameInput.setAttribute('type', 'text');
    filenameInput.setAttribute('name', 'name');

    var typeInput = document.createElement('select');
    form.appendChild(typeInput);
    typeInput.className = 'four column';
    typeInput.required = true;

    typeInput.appendChild(_createOption("", "---------"));
    typeInput.appendChild(_createOption(1, "Student Handout"));
    typeInput.appendChild(_createOption(2, "Teacher Reference"));
    typeInput.appendChild(_createOption(3, "Slides"));
    typeInput.appendChild(_createOption(4, "Code"));
    typeInput.appendChild(_createOption(5, "Schematic"));
    typeInput.appendChild(_createOption(0, "Other"));

    var removeIcon = document.createElement('i');
    form.appendChild(removeIcon);
    removeIcon.className = 'one column icon-remove';

    var that = this;
    $(removeIcon).click(function(ev) {
        that.onRemove(ev).then(function(_) {
            $(form).remove();
        });
    });

    var progressBar = document.createElement('progress');
    form.appendChild(progressBar);
    progressBar.className = 'progress-bar whole column';

    this.progressBar = progressBar;
    this.form = form;
}

ResourceForm.prototype.setParent = function(element) {
    $(element).append(this.form);
};

ResourceForm.prototype.getProgressBar = function() {
    return this.progressBar;
}

function patchResource(id, data) {
    return new Promise(function(resolve, reject) {
        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function(event) {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.response.hasOwnProperty('success')) {
                    resolve(data);
                } else {
                    reject(xhr.response['err']);
                }
            }
        };

        xhr.open('PUT', '/lesson-resource/' + id + '/', true);
        xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.responseType = 'json';
        xhr.send(JSON.stringify(data));
    });
}

function submitLessonPlan(event) {
    event.preventDefault();

    var allowSubmission = true;

    var resources = document.getElementsByClassName('lesson-resource-form');
    for(var index = 0; index < resources.length; ++index) {
        var form = resources[index];
        if(form.dataset.resourceId === undefined) {
            // Upload not finished, or failed!
            allowSubmission = false;
        }
        allowSubmission = allowSubmission && form.reportValidity();
    }

    var lessonPlanForm = document.getElementById('lesson-plan-form');
    allowSubmission = allowSubmission && lessonPlanForm.reportValidity();

    var resourceIds = [];
    if(allowSubmission) {
        var promises = [];
        for(var index = 0; index < resources.length; ++index) {
            var form = resources[index];
            // Make a request to the server, given ID
            var resourcePatch = {
                name: form.elements[0].value,
                type: form.elements[1].value
            };
            resourceIds.push(form.dataset.resourceId);
            promises.push(patchResource(form.dataset.resourceId, resourcePatch));
        }
        Promise.all(promises).then(function(values) {
            var resourceIdsInput = document.createElement('input');
            resourceIdsInput.setAttribute('name', 'resources');
            resourceIdsInput.setAttribute('type', 'hidden');
            resourceIdsInput.setAttribute('value', resourceIds.join(','));
            lessonPlanForm.appendChild(resourceIdsInput);
            lessonPlanForm.submit();
        });
    }
}

$(function(e) {
    var curriculumClient = new CurriculumClient(window.CSRF_TOKEN);
    var fileSelect = document.getElementById('file-select');
    fileSelect.addEventListener('change', function(event) {
        var files = fileSelect.files;
        for(var index = 0; index < files.length; ++index) {
            var file = files[index];
            let form = new ResourceForm(file.name);

            var idPromise = curriculumClient.uploadResource(file, {
                progress: form.getProgressBar()
            });

            idPromise.then(function(id) {
                form.form.dataset.resourceId = id;
            })

            form.onRemove = function(_) {
                return idPromise.then(function(id) {
                    return curriculumClient.deleteResource(id);                
                });
            };

            form.setParent('#lesson-resource-forms');
        }
    });

    var submitLessonPlanBtn = document.getElementById('submit-lesson-plan');
    submitLessonPlanBtn.addEventListener('click', submitLessonPlan);
});
