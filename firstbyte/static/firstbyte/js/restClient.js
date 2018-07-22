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
    const endpoint = defaultValue(options.endpoint, '/lesson-resources/');
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
                            var current = progressEvent.loaded;
                            var max = progressEvent.total;
                            var currentPercentage = current / max * 100.0;
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
        .done(function(response, textStatus, jqXHR) {
            if(defined(response.id)) {
                $(progress).removeClass('bg-info').addClass('bg-success');
                resolve(response.id);
            } else {
                $(progress).removeClass('bg-info').addClass('bg-danger');
                reject(response.err);
            }
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
           _rejectJqueryAjax(reject, errorThrown, textStatus);
        });
    });
};

CurriculumClient.prototype.putResource = function(id, data, options) {
    options = options || {};
    const endpoint = defaultValue(options.endpoint, '/lesson-resources/' + id + '/');

    var that = this;
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
        .then(function(response, textStatus, jqXHR) {
            resolve(response);
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            _rejectJqueryAjax(reject, errorThrown, textStatus);
        });
    });
}
CurriculumClient.prototype.deleteResource = function(id, options) {
    options = options || {};
    const endpoint = defaultValue(options.endpoint, '/lesson-resources/' + id + '/');

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