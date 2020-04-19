'use strict';

import $ from 'jquery';

import Vue from 'vue';

import { BootstrapVue } from 'bootstrap-vue';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import TheCurriculumForm from './components/TheCurriculumForm.vue';

import CurriculumClient from './curriculumClient.js';

import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlusCircle, faMinusCircle, faAlignJustify } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

$(() => {
    library.add(faPlusCircle);
    library.add(faMinusCircle);
    library.add(faAlignJustify);

    Vue.use(BootstrapVue);

    Vue.component('font-awesome-icon', FontAwesomeIcon);

    Vue.prototype.$curriculumForm = {
        client: new CurriculumClient(window.CSRF_TOKEN),
        updatingCurriculumId: window.CURRICULUM_ID,
    };

    new Vue({
        el: "#vue-container",
        components: {
            TheCurriculumForm,
        },
    });
});
