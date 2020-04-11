'use strict';

import $ from 'jquery';

import Vue from 'vue';

import { BootstrapVue } from 'bootstrap-vue';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import TheCurriculumForm from './components/TheCurriculumForm.vue';

import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlusCircle, faMinusCircle, faGripLinesVertical } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

$(() => {
    library.add(faPlusCircle);
    library.add(faMinusCircle);
    library.add(faGripLinesVertical);

    Vue.use(BootstrapVue);

    Vue.component('font-awesome-icon', FontAwesomeIcon);

    new Vue({
        el: "#vue-container",
        components: {
            TheCurriculumForm
        }
    });
});
