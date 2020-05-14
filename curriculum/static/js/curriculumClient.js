'use strict';

import axios from 'axios';

function defined(val) {
    return val !== undefined;
}

function defaultValue(val, fallback) {
    if(defined(val)) return val;
    return fallback;
}

export default function CurriculumClient(csrfToken) {
    this.csrfToken = csrfToken;
}

CurriculumClient.prototype.submitLessonPlan = async function(combinedFormData, options) {
    options = options || {};
    const endpoint = defaultValue(options.endpoint, '/api/v2/lesson-plans/');
    const method = defaultValue(options.method, 'POST');

    return await axios({
        method: method,
        url: endpoint,
        data: combinedFormData,
        headers: {
            'X-CSRFToken': this.csrfToken,
        },
    });
};

CurriculumClient.prototype.updateLessonPlan = function(combinedFormData, id, options) {
    options = options || {};
    options.endpoint = defaultValue(options.endpoint, '/api/v2/lesson-plans/' + id + '/');
    options.method = defaultValue(options.method, 'PUT');
    return this.submitLessonPlan(combinedFormData, options);
};