'use strict';

import $ from 'jquery';

import Vue from 'vue';

import { BootstrapVue } from 'bootstrap-vue'

import TheCurriculumForm from './components/TheCurriculumForm.vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

$(() => {
    Vue.use(BootstrapVue)

    var vm = new Vue({
        el: "#vue-container",
        components: {
            TheCurriculumForm
        }
    });
});
