'use strict';

import $ from 'jquery';

import Vue from 'vue';

import { BootstrapVue } from 'bootstrap-vue';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import TheCurriculumForm from './components/TheCurriculumForm.vue';

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

$(() => {
    Vue.use(BootstrapVue);

    Vue.component('font-awesome-icon', FontAwesomeIcon);

    new Vue({
        el: "#vue-container",
        components: {
            TheCurriculumForm
        }
    });
});
