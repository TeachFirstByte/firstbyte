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

CurriculumClient.prototype.uploadResource = function (file, options) {
    options = options || {};
    const endpoint = defaultValue(options.endpoint, '/lesson-resource/');
    const progress = options.progress;

    const formData = new FormData();
    formData.append('file', file, file.name);

    var that = this;
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
                var myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload && defined(progress)) {
                    myXhr.upload.addEventListener('progress', function(progressEvent) {
                        if(progressEvent.lengthComputable) {
                            $(progress).attr({
                                value: progressEvent.loaded,
                                max: progressEvent.total,
                            });
                        }
                    });
                }
                return myXhr;
            }
        })
        .done(function(response, textStatus, jqXHR) {
            if(defined(response.id)) {
                resolve(response.id);
            } else {
                reject(response.err);
            }
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
           _rejectJqueryAjax(reject, errorThrown, textStatus);
        });
    });
};

CurriculumClient.prototype.deleteResource = function(id, options) {
    options = options || {};
    const endpoint = defaultValue(options.endpoint, '/lesson-resource/' + id + '/');

    var that = this;
    return new Promise(function(resolve, reject) {
        $.ajax(endpoint, {
            method: 'DELETE',
            dataType: 'json',
            cache: false,
            headers: {
                'X-CSRFToken': that.csrfToken
            }
        })
        .then(function(response, textStatus, jqXHR) {
            resolve(response);
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            _rejectJqueryAjax(reject, errorThrown, textStatus);
        });
    });
}

function _rejectJqueryAjax(reject, errorThrown, textStatus) {
    if(defined(errorThrown)) {
        reject(new Error(errorThrown));
    } else {
        reject(new Error(textStatus));
    }
}