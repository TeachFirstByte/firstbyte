'use strict';

import $ from 'jquery';

$(document).ready(function() {
    $(".card-hover-shadow").hover(
        function() {
            $(this).addClass('shadow').css('cursor', 'pointer');
        },
        function() {
            $(this).removeClass('shadow');
        }
    );
});
