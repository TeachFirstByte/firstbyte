'use strict';

import $ from 'jquery';
import Promise from 'bluebird';

import FileUpload from './fileUpload.js';
import { CurriculumClient } from './restClient.js';
import Droparea from './droparea.js';

var resourceForm = '\
<form data-lr-form method="post" enctype="multipart/form-data"> \
    <div class="row"> \
        <div class="col"> \
            <span data-lr-error-message></span> \
        </div> \
    </div> \
    <div class="row mb-2"> \
        <div class="input-group col"> \
            <select required name="type" class="form-control rounded-left" data-lr-type-value> \
                <option value="">---------</option> \
                <option value="1">Student Handout</option> \
                <option value="2">Teacher Reference</option> \
                <option value="3">Slides</option> \
                <option value="4">Code</option> \
                <option value="5">Schematic</option> \
                <option value="0">Other</option> \
            </select> \
            <input required type="text" name="name" class="form-control text-left" data-lr-name-value > \
            <div class="input-ground-append"> \
                <button class="btn btn-outline-danger" data-lr-remove>Remove</button> \
            </div> \
        </div> \
    </div> \
    <input type="hidden" name="resourceId" value="" data-lr-resource-id />\
</form>';

var curriculumClient;
var fileUpload;
var droparea;

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
    fileUpload = new FileUpload({
        container: '#lesson-resources',
        template: resourceForm,
    });

    var updatingLessonPlan = false;
    if(window.LESSON_PLAN_ID !== undefined) {
        updatingLessonPlan = true;
    }

    if(updatingLessonPlan) {
        curriculumClient.getLessonPlan(window.LESSON_PLAN_ID).then(function(lessonplan) {
            for (var i = 0; i < lessonplan.resources.length; ++i) {
                var resource = lessonplan.resources[i];
                fileUpload.addExistingSlot(resource.id, resource.semantic_type, resource.name);
            }
        }).catch(function(err) {
            console.log(err);
        });
    }

    // Set up all the ways the user can add a file:
    // 1. Drag and drop area
    droparea = new Droparea('.lr-droparea', fileUpload.addFileSlot.bind(fileUpload));

    // 2. By clicking the dropzone
    droparea.element.on('click', function(event) {
        if($(this).is(event.target)) {
            $('.lr-file-input').trigger('click');
        }
    });

    // 3. By clicking on the message above the droparea (in case the marked off area gets full).
    $('.lr-additional-clickarea').on('click', function(event) {
        if($(this).is(event.target)) {
            $('.lr-file-input').trigger('click');
        }
    });

    // Helper for making clicks open up a file dialog
    $('.lr-file-input').on('change', function(event) {
        var files = event.currentTarget.files;
        for(var index = 0; index < files.length; ++index) {
            var file = files[index];
            fileUpload.addFileSlot(file);
        }
    });

    $('#submit-lesson-plan').on('click', function(event) {
        event.preventDefault();

        var form = document.getElementById('lesson-plan-form');

        if(!form.reportValidity()) {
            return;
        }

        var allFormsAreValid = true;
        fileUpload.forEach(function(_, resourceForm){
            allFormsAreValid = allFormsAreValid && resourceForm.reportValidity();
        });
        if(!allFormsAreValid) {
            return;
        }

        var resourceIds = [];
        var filetypes = [];
        var filenames = [];
        var files = [];
        fileUpload.forEach(function(file, form) {
            var formData = new FormData(form);
            resourceIds.push(formData.get('resourceId') || '')
            filetypes.push(formData.get('type'));
            filenames.push(formData.get('name'));
            files.push(file);
        });

        // At this point we have three arrays with lesson resource info split between them.
        // We have a lot of options:
        // - Add these arrays to the <form> and submit (browser handles redirect)
        //   - Doesn't work - can't construct an <input type="file"> and populate it with our arbitrary list.
        // - Build our own formData (starting from the main lesson plan form as a base)
        // then add lesson resources and submit as one form via AJAX, then redirect the user.
        // This way we could probably have some sort of loading bar for the entire form as a whole
        // (to represent all the lesson resource files that are being uploaded, I'm not sure if we can do each file individually).
        // - Submit lesson plan and request a certain number of lesson resource slots, then upload those files individually and redirect via JS

        var lessonPlanFormData = new FormData(form);
        lessonPlanFormData.append('resource_ids', resourceIds.join());
        lessonPlanFormData.append('filetypes', filetypes.join());

        // Better make sure filenames don't have a comma, otherwise this will break badly.
        lessonPlanFormData.append('filenames', filenames.join());

        for(var i = 0; i < files.length; ++i) {
            lessonPlanFormData.append('files[]', files[i]);
        }

        // Request a json response
        lessonPlanFormData.set('jsonResponse', true);

        var submissionPromise;
        if (updatingLessonPlan) {
            submissionPromise = curriculumClient.updateLessonPlan(lessonPlanFormData, window.LESSON_PLAN_ID);
        } else {
            submissionPromise = curriculumClient.submitLessonPlan(lessonPlanFormData);
        }

        submissionPromise.then(function(response) {
            window.location.href = '/lesson-plans/' + response.id;
        }).catch(function(error) {
            // Post this error for the user.
            console.error(error);
        });
    });
});
