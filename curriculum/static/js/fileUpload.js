'use strict';

import $ from 'jquery';

export default function FileUpload(options) {
    this.element = $(options.container);
    this.element.children('.lr-fallback').remove();

    this.template = options.template;

    this.slots = [];
}

FileUpload.prototype.addFileSlot = function(file) {
    let that = this;

    let templateInstance = $(this.template);

    // Add filename to text box value
    let takesFileNameAsValue = templateInstance.find('[data-lr-name-value]');
    takesFileNameAsValue.attr('value', file.name);

    this.element.prepend(templateInstance);

    // The template may have a root <form> element, so we need to use addBack to include it in that case.
    let form = templateInstance.find('[data-lr-form]').addBack('[data-lr-form]')[0];

    let slot = {
        file: file,
        form: form,
        templateInstance: templateInstance,
    };

    // Activate remove button
    let removeButton = templateInstance.find('[data-lr-remove]');
    removeButton.click(function(event) {
        that.removeSlot(slot);
        event.stopPropagation();
    });

    this.slots.push(slot);
};

FileUpload.prototype.addExistingSlot = function(id, type, name) {
    let that = this;

    let templateInstance = $(this.template);

    let takesResourceIdAsValue = templateInstance.find('[data-lr-resource-id]');
    takesResourceIdAsValue.attr('value', id);

    let takesFileTypeAsValue = templateInstance.find('[data-lr-type-value]');
    takesFileTypeAsValue.val(type);

    let takesFileNameAsValue = templateInstance.find('[data-lr-name-value]');
    takesFileNameAsValue.attr('value', name);

    this.element.prepend(templateInstance);

    // The template may have a root <form> element, so we need to use addBack to include it in that case.
    let form = templateInstance.find('[data-lr-form]').addBack('[data-lr-form]')[0];

    let slot = {
        file: null,
        form: form,
        templateInstance: templateInstance,
    };

    // Activate remove button
    let removeButton = templateInstance.find('[data-lr-remove]');
    removeButton.click(function(event) {
        that.removeSlot(slot);
        event.stopPropagation();
    });

    this.slots.push(slot);
};

FileUpload.prototype.removeSlot = function(slot) {
    slot.templateInstance.remove();
    let index = this.slots.indexOf(slot);
    this.slots.splice(index, 1);
};

// Callback takes in file and form.
FileUpload.prototype.forEach = function(callback) {
    for(let i = 0; i < this.slots.length; ++i) {
        let slot = this.slots[i];
        callback(slot.file, slot.form);
    }
};
