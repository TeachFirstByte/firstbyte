'use strict';

import $ from 'jquery'

export default function FileUpload(options) {
    this.element = $(options.container);
    this.element.children('.lr-fallback').remove();

    this.template = options.template;

    this.slots = [];
}

FileUpload.prototype.addFileSlot = function(file) {
    var that = this;

    var templateInstance = $(this.template);

    // Add filename to text box value
    var takesFileNameAsValue = templateInstance.find('[data-lr-name-value]');
    takesFileNameAsValue.attr('value', file.name);

    this.element.prepend(templateInstance);

    // The template may have a root <form> element, so we need to use addBack to include it in that case.
    var form = templateInstance.find('[data-lr-form]').addBack('[data-lr-form]')[0];

    var slot = {
        file: file,
        form: form,
        templateInstance: templateInstance,
    };

    // Activate remove button
    var removeButton = templateInstance.find('[data-lr-remove]');
    removeButton.click(function(event) {
        that.removeSlot(slot);
        event.stopPropagation();
    });

    this.slots.push(slot);
};

FileUpload.prototype.addExistingSlot = function(id, type, name) {
    var that = this;

    var templateInstance = $(this.template);

    var takesResourceIdAsValue = templateInstance.find('[data-lr-resource-id]');
    takesResourceIdAsValue.attr('value', id);

    var takesFileTypeAsValue = templateInstance.find('[data-lr-type-value]');
    takesFileTypeAsValue.val(type);

    var takesFileNameAsValue = templateInstance.find('[data-lr-name-value]');
    takesFileNameAsValue.attr('value', name);

    this.element.prepend(templateInstance);

    // The template may have a root <form> element, so we need to use addBack to include it in that case.
    var form = templateInstance.find('[data-lr-form]').addBack('[data-lr-form]')[0];

    var slot = {
        file: null,
        form: form,
        templateInstance: templateInstance,
    };

    // Activate remove button
    var removeButton = templateInstance.find('[data-lr-remove]');
    removeButton.click(function(event) {
        that.removeSlot(slot);
        event.stopPropagation();
    });

    this.slots.push(slot);
}

FileUpload.prototype.removeSlot = function(slot) {
    slot.templateInstance.remove();
    var index = this.slots.indexOf(slot);
    this.slots.splice(index, 1);
};

// Callback takes in file and form.
FileUpload.prototype.forEach = function(callback) {
    for(var i = 0; i < this.slots.length; ++i) {
        var slot = this.slots[i];
        callback(slot.file, slot.form);
    }
}
