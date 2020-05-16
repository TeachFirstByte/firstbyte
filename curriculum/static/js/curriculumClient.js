'use strict';

import axios from 'axios';

export async function submitCurriculum(config) {
    config = config || {};
    config.url = config.url || '/api/v2/lesson-plans/';
    config.method = config.method || 'post';

    return await axios(config);
}

export function updateCurriculum(id, config) {
    config = config || {};
    config.url = config.url || '/api/v2/lesson-plans/' + id + '/';
    config.method = config.method || 'put';
    return submitCurriculum(config);
}

export async function getCurriculum(id, config) {
    config = config || {};
    config.url = config.url || '/api/v2/lesson-plans/' + id + '/';
    config.method = config.method || 'get';

    const response = await axios(config);
    return response.data;
}