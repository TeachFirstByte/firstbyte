'use strict';

function addTimeBoxChild(container, className, flexGrow) {
    var box = document.createElement('div');
    box.className = className;

    // Give it some size (actual size relative to the sum of flexGrow of all siblings).
    box.style.flexGrow = flexGrow;

    container.appendChild(box);
}

window.addEventListener('DOMContentLoaded', function() {
    // Fill in all time box containers
    var res = document.getElementsByClassName("time-box-container");
    for(var i = 0; i < res.length; ++i) {
        var timeBox = res[i];

        // How much time are we representing?
        var totalTime = parseFloat(timeBox.dataset.prepTime) + parseFloat(timeBox.dataset.classTime);

        // 1 minute = 1 pixel
        timeBox.style.width = (totalTime / 60) + "em";

        // Add blank box
        addTimeBoxChild(timeBox, 'blank-time-box', timeBox.dataset.prepTime);

        // Add filled box
        addTimeBoxChild(timeBox, 'filled-time-box', timeBox.dataset.classTime);

        // Show the time box
        timeBox.style.display = 'flex';
    }
});
