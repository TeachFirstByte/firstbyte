'use strict';

import $ from 'jquery';

$(function() {
    $('[data-average-rating]').each(function(index, element) {
        var container = $(element);
        var averageRating = $(container).attr('data-average-rating');

        var numFilledStars = Math.floor(averageRating);
        var extra = averageRating - numFilledStars;
        if(extra >= .75) {
            numFilledStars += 1;
            extra = 0.0;
        } else if (extra <= .25) {
            extra = 0.0;
        }
        container.children('.fa-star').each(function(starNum, element) {
            var starElement = $(element);
            if(starNum < numFilledStars) {
                // Star completely filled in
                starElement.addClass('fas');
            } else if(starNum === numFilledStars && extra > 0) {
                // Half-filled
                starElement.removeClass('fa-star').addClass('fas').addClass('fa-star-half-alt');
            } else {
                // Outline
                starElement.addClass('far');
            }
        });
    });
});