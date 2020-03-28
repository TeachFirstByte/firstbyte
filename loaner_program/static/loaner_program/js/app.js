'use strict';

import $ from 'jquery';

import Vue from 'vue';
import TheLoanerProgram from './components/TheLoanerProgram.vue'

$(() => {
    new Vue({
        el: "#vue-container",
        components: {
            TheLoanerProgram
        }
    });
});
