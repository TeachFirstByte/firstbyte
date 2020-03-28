'use strict';

import $ from 'jquery';

export default function Droparea(selector, callback, classNameOverrides) {
    this.element = $(selector);
    this.callback = callback;

    classNameOverrides = classNameOverrides || {};
    this.classNames = {
        'pending-drop': classNameOverrides['pending-drop'] || 'lr-pending-drop'
    };

    this.element.on('drop', this.onDropHandler.bind(this));
    this.element.on('dragover', this.onDragOverHandler.bind(this));
    this.element.on('dragenter', this.onDragEnterHandler.bind(this));
    this.element.on('dragleave', this.onDragExitHandler.bind(this));
}

Droparea.prototype.onDropHandler = function(event) {
    event.preventDefault();

    let originalEvent = event.originalEvent;

    if (originalEvent.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
        for (let i = 0; i < originalEvent.dataTransfer.items.length; i++) {
            // If dropped items aren't files, reject them
            if (originalEvent.dataTransfer.items[i].kind === 'file') {
                let file = originalEvent.dataTransfer.items[i].getAsFile();
                this.callback(file);
            }
        }
        originalEvent.dataTransfer.items.clear();

    } else {
        // Use DataTransfer interface to access the file(s)
        for (let i = 0; i < originalEvent.dataTransfer.files.length; i++) {
            let file = originalEvent.dataTransfer.files[i];
            this.callback(file);
        }

        originalEvent.dataTransfer.clearData();
    }
    // We've handled the drag
    this.onDragExitHandler();
};

Droparea.prototype.onDragOverHandler = function(event) {
    event.preventDefault();
};

Droparea.prototype.onDragEnterHandler = function() {
    this.element.addClass(this.classNames['pending-drop']);
};
Droparea.prototype.onDragExitHandler = function() {
    this.element.removeClass(this.classNames['pending-drop']);
};