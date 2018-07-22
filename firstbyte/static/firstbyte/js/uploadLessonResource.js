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
    form.className = 'mb-2 lesson-resource-form';
    form.setAttribute('method', 'post');
    form.setAttribute('enctype', 'multipart/form-data');

    var firstRow = document.createElement('div');
    firstRow.className = 'row';
    form.appendChild(firstRow);

    var secondRow = document.createElement('div');
    secondRow.className = 'row';
    form.appendChild(secondRow);

    var inputGroup = document.createElement('div');
    firstRow.appendChild(inputGroup);
    inputGroup.className = 'input-group col';

    var typeInput = document.createElement('select');
    inputGroup.appendChild(typeInput);
    typeInput.className = 'form-control rounded-left';
    typeInput.required = true;

    typeInput.appendChild(_createOption("", "---------"));
    typeInput.appendChild(_createOption(1, "Student Handout"));
    typeInput.appendChild(_createOption(2, "Teacher Reference"));
    typeInput.appendChild(_createOption(3, "Slides"));
    typeInput.appendChild(_createOption(4, "Code"));
    typeInput.appendChild(_createOption(5, "Schematic"));
    typeInput.appendChild(_createOption(0, "Other"));

    var filenameInput = document.createElement('input');
    inputGroup.appendChild(filenameInput);
    filenameInput.className = 'form-control';
    filenameInput.value = filename;
    filenameInput.setAttribute('type', 'text');
    filenameInput.setAttribute('name', 'name');

    var btnContainer = document.createElement('div');
    inputGroup.appendChild(btnContainer);
    btnContainer.className = 'input-group-append';

    var removeBtn = document.createElement('button');
    btnContainer.appendChild(removeBtn);
    removeBtn.className = 'btn btn-outline-danger';
    removeBtn.innerText = "Remove";

    var that = this;
    $(removeBtn).click(function(ev) {
        that.onRemove(ev).then(function(_) {
            $(form).remove();
        });
    });

    var progressCol = document.createElement('div');
    secondRow.appendChild(progressCol);
    progressCol.className = 'col';

    var progress = document.createElement('div');
    progressCol.appendChild(progress);
    progress.className = 'progress';

    var progressBar = document.createElement('div');
    progress.append(progressBar);
    progressBar.className = 'progress-bar bg-info';
    progressBar.setAttribute('role', 'progressbar');
    progressBar.setAttribute('aria-valuenow', '0');
    progressBar.setAttribute('aria-valuemin', '0');
    progressBar.setAttribute('aria-valuemax', '100');

    this.progressBar = progressBar;
    this.form = form;
}

ResourceForm.prototype.setParent = function(element) {
    $(element).append(this.form);
};

ResourceForm.prototype.getProgressBar = function() {
    return this.progressBar;
}

var curriculumClient;

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
                name: form.elements[1].value,
                type: form.elements[0].value
            };
            resourceIds.push(form.dataset.resourceId);
            promises.push(curriculumClient.putResource(form.dataset.resourceId, resourcePatch));
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
    curriculumClient = new CurriculumClient(window.CSRF_TOKEN);
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
