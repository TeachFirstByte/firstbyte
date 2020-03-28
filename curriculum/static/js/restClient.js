'use strict';

import $ from 'jquery';
import Promise from 'bluebird';

function defined(val) {
    return val !== undefined;
}

function defaultValue(val, fallback) {
    if(defined(val)) return val;
    return fallback;
}

export function CurriculumClient(csrfToken) {
    this.csrfToken = csrfToken;
}

CurriculumClient.prototype.submitLessonPlan = function(combinedFormData, options) {
    options = options || {};
    const endpoint = defaultValue(options.endpoint, '/lesson-plans/new/');

    let that = this;
    return new Promise(function(resolve, reject) {
        $.ajax(endpoint, {
            method: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': that.csrfToken
            },
            contentType: false,
            processData: false,
            cache: false,
            data: combinedFormData,
        })
        .done(function(response, _textStatus, _jqXHR) {
            resolve(response);
        })
        .fail(function(jqXHR, _textStatus, errorThrown) {
            // Form errors can be found in the response.
            // Just parse the JSON and check the form_errors field.
            _rejectJqueryAjax(reject, errorThrown, jqXHR.responseText);
        });
    });
}

CurriculumClient.prototype.updateLessonPlan = function(combinedFormData, id, options) {
    options = options || {};
    options.endpoint = defaultValue(options.endpoint, '/lesson-plans/update/' + id + '/');
    return this.submitLessonPlan(combinedFormData, options);
};

CurriculumClient.prototype.uploadResource = function (file, options) {
    options = options || {};
    const endpoint = defaultValue(options.endpoint, '/lesson-resources/');
    const progress = options.progress;

    const formData = new FormData();
    formData.append('file', file, file.name);

    let that = this;
    return new Promise(function(resolve, reject) {
        $.ajax(endpoint, {
            method: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': that.csrfToken
            },
            contentType: false,
            processData: false,
            cache: false,
            data: formData,

            xhr: function() {
                let myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload && defined(progress)) {
                    myXhr.upload.addEventListener('progress', function(progressEvent) {
                        if(progressEvent.lengthComputable) {
                            let current = progressEvent.loaded;
                            let max = progressEvent.total;
                            let currentPercentage = current / max * 100.0;
                            $(progress).attr({
                                'aria-valuenow': progressEvent.loaded,
                                'aria-valuemax': progressEvent.total,
                                style: 'width: ' + currentPercentage + '%;'
                            });
                        }
                    });
                }
                return myXhr;
            }
        })
        .done(function(response, _textStatus, _jqXHR) {
            if(defined(response.id)) {
                $(progress).removeClass('bg-info').addClass('bg-success');
                resolve(response.id);
            } else {
                $(progress).removeClass('bg-info').addClass('bg-danger');
                reject(response);
            }
        })
        .fail(function(jqXHR, _textStatus, errorThrown) {
           _rejectJqueryAjax(reject, errorThrown, jqXHR.responseText);
        });
    });
};

CurriculumClient.prototype.putResource = function(id, data, options) {
    options = options || {};
    const endpoint = defaultValue(options.endpoint, '/lesson-resources/' + id + '/');

    let that = this;
    return new Promise(function(resolve, reject) {
        $.ajax(endpoint, {
            method: 'PUT',
            dataType: 'json',
            contentType: 'application/json',
            processData: false,
            cache: false,
            headers: {
                'X-CSRFToken': that.csrfToken
            },
            data: JSON.stringify(data)
        })
        .then(function(response, _textStatus, _jqXHR) {
            resolve(response);
        })
        .fail(function(jqXHR, _textStatus, errorThrown) {
            _rejectJqueryAjax(reject, errorThrown, jqXHR.responseText);
        });
    });
}
CurriculumClient.prototype.deleteResource = function(id, options) {
    options = options || {};
    const endpoint = defaultValue(options.endpoint, '/lesson-resources/' + id + '/');

    let that = this;
    return new Promise(function(resolve, reject) {
        $.ajax(endpoint, {
            method: 'DELETE',
            dataType: 'json',
            cache: false,
            headers: {
                'X-CSRFToken': that.csrfToken
            }
        })
        .then(function(response, _textStatus, _jqXHR) {
            resolve(response);
        })
        .fail(function(jqXHR, _textStatus, errorThrown) {
            _rejectJqueryAjax(reject, errorThrown, jqXHR.responseText);
        });
    });
}

CurriculumClient.prototype.getLessonPlan = function(id, options) {
    options = options || {};
    const endpoint = defaultValue(options.endpoint, '/api/v1/lesson-plans/' + id + '/');

    return new Promise(function(resolve, reject) {
        $.ajax(endpoint, {
            dataType: 'json',
        })
        .then(function(response, _textStatus, _jqXHR) {
            resolve(response);
        })
        .fail(function(jqXHR, _textStatus, errorThrown) {
            _rejectJqueryAjax(reject, errorThrown, jqXHR.responseText);
        });
    });
}

function _rejectJqueryAjax(reject, errorThrown, textStatus) {
    if(defined(errorThrown)) {
        reject(new Error(textStatus));
    } else {
        reject(new Error(textStatus));
    }
}
