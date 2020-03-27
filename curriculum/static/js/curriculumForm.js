'use strict';

import $ from 'jquery';

import Vue from 'vue';
import TheCurriculumForm from './components/TheCurriculumForm.vue'

$(() => {
    var vm = new Vue({
        el: "#vue-container",
        components: {
            TheCurriculumForm
        }
    });
});
