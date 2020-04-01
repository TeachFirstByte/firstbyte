'use strict';

import $ from 'jquery';

import Vue from 'vue';

import { BootstrapVue } from 'bootstrap-vue';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import TheCurriculumForm from './components/TheCurriculumForm.vue';


$(() => {
    Vue.use(BootstrapVue);

    new Vue({
        el: "#vue-container",
        components: {
            TheCurriculumForm
        }
    });
});
