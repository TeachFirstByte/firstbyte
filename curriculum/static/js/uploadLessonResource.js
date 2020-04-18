'use strict';

import $ from 'jquery';
import Promise from 'bluebird';

import FileUpload from './fileUpload.js';
import { CurriculumClient } from './restClient.js';
import Droparea from './droparea.js';

let resourceForm = '\
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

let curriculumClient;
let fileUpload;
let droparea;

// eslint-disable-next-line no-unused-vars
function submitLessonPlan(event) {
    event.preventDefault();

    let allowSubmission = true;

    let resources = document.getElementsByClassName('lesson-resource-form');
    for(let index = 0; index < resources.length; ++index) {
        let form = resources[index];
        if(form.dataset.resourceId === undefined) {
            // Upload not finished, or failed!
            allowSubmission = false;
        }
        allowSubmission = allowSubmission && form.reportValidity();
    }

    let lessonPlanForm = document.getElementById('lesson-plan-form');
    allowSubmission = allowSubmission && lessonPlanForm.reportValidity();

    let resourceIds = [];
    if(allowSubmission) {
        let promises = [];
        for(let index = 0; index < resources.length; ++index) {
            let form = resources[index];
            // Make a request to the server, given ID
            let resourcePatch = {
                name: form.elements[1].value,
                type: form.elements[0].value,
            };
            resourceIds.push(form.dataset.resourceId);
            promises.push(curriculumClient.putResource(form.dataset.resourceId, resourcePatch));
        }
        Promise.all(promises).then(function(_values) {
            let resourceIdsInput = document.createElement('input');
            resourceIdsInput.setAttribute('name', 'resources');
            resourceIdsInput.setAttribute('type', 'hidden');
            resourceIdsInput.setAttribute('value', resourceIds.join(','));
            lessonPlanForm.appendChild(resourceIdsInput);
            lessonPlanForm.submit();
        });
    }
}

$(function(_) {
    curriculumClient = new CurriculumClient(window.CSRF_TOKEN);
    fileUpload = new FileUpload({
        container: '#lesson-resources',
        template: resourceForm,
    });

    let updatingLessonPlan = false;
    if(window.LESSON_PLAN_ID !== undefined) {
        updatingLessonPlan = true;
    }

    if(updatingLessonPlan) {
        curriculumClient.getLessonPlan(window.LESSON_PLAN_ID).then(function(lessonplan) {
            for (let i = 0; i < lessonplan.resources.length; ++i) {
                let resource = lessonplan.resources[i];
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
        let files = event.currentTarget.files;
        for(let index = 0; index < files.length; ++index) {
            let file = files[index];
            fileUpload.addFileSlot(file);
        }
    });

    $('#submit-lesson-plan').on('click', function(event) {
        event.preventDefault();

        let form = document.getElementById('lesson-plan-form');

        if(!form.reportValidity()) {
            return;
        }

        let allFormsAreValid = true;
        fileUpload.forEach(function(_, resourceForm){
            allFormsAreValid = allFormsAreValid && resourceForm.reportValidity();
        });
        if(!allFormsAreValid) {
            return;
        }

        let resourceIds = [];
        let filetypes = [];
        let filenames = [];
        let files = [];
        fileUpload.forEach(function(file, form) {
            let formData = new FormData(form);
            resourceIds.push(formData.get('resourceId') || false);
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

        let lessonPlanFormData = new FormData(form);
        lessonPlanFormData.append('resource_ids', JSON.stringify(resourceIds));
        lessonPlanFormData.append('filetypes', JSON.stringify(filetypes));

        // Better make sure filenames don't have a comma, otherwise this will break badly.
        lessonPlanFormData.append('filenames', JSON.stringify(filenames));

        for(let i = 0; i < files.length; ++i) {
            lessonPlanFormData.append('files[]', files[i]);
        }

        // Request a json response
        lessonPlanFormData.set('jsonResponse', true);

        let submissionPromise;
        if (updatingLessonPlan) {
            submissionPromise = curriculumClient.updateLessonPlan(lessonPlanFormData, window.LESSON_PLAN_ID);
        } else {
            submissionPromise = curriculumClient.submitLessonPlan(lessonPlanFormData);
        }

        submissionPromise.then(function(response) {
            window.location.href = '/lesson-plans/' + response.id;
        }).catch(function(error) {
            let obj = JSON.parse(error.message);
            for(let key in obj) {
                if(Object.prototype.hasOwnProperty.call(obj, key)) {
                    let elem = $('[name="' + key +'"]')[0];
                    let num_errors = obj[key].length;
                    elem.setCustomValidity(obj[key][num_errors - 1]);
                }
            }
        });
    });
});
