<template>
    <b-row fluid="mb-2">
        <b-col>
            <b-input-group>
                <b-input-group-prepend>
                    <b-form-select
                        class="lesson-resource-type-select"
                        variant="primary"
                        :options="typeOptions"
                        :state="getBootstrapFormInputState(vuelidateObject.type)"
                        :value="type"
                        @input="$emit('update:type', $event)"
                    />
                </b-input-group-prepend>
                <b-form-input
                    type="text"
                    :state="getBootstrapFormInputState(vuelidateObject.name)"
                    :value="name"
                    @input="$emit('update:name', $event)"
                />
                <b-input-group-append>
                    <b-button
                        class="remove-btn"
                        variant="danger"
                        aria-label="Remove"
                        @click="$emit('onRemove')"
                    >
                        <span aria-hidden="true">&times;</span>
                    </b-button>
                </b-input-group-append>
            </b-input-group>
        </b-col>
    </b-row>
</template>
<script>
    import { getBootstrapFormInputState } from '../componentUtil.js';

    export const TYPE_OPTIONS = [
        { value: null, text: ""},
        { value: 1, text: "Student Handout"},
        { value: 2, text: "Teacher Reference"},
        { value: 3, text: "Slides"},
        { value: 4, text: "Code"},
        { value: 5, text: "Schematic"},
        { value: 0, text: "Other"},
    ];

    export default {
        props: {
            name: {
                type: String,
                default: "",
            },
            type: {
                type: Number,
                default: null,
            },
            vuelidateObject: {
                type: Object,
                default: () => {return {}; },
            },
        },
        data() {
            return {
                typeOptions: TYPE_OPTIONS,
                getBootstrapFormInputState,
            };
        },
    };
</script>
<style lang="scss" scoped>
    .remove-btn {
        padding: 0 6px;
    }
    .lesson-resource-type-select {
        border-top-right-radius: 0px;
        border-bottom-right-radius: 0px;

        width: 13em;

        &:focus {
            z-index: 2;
        }
    }
</style>