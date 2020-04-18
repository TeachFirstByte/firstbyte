<template>
    <b-row fluid="mb-2">
        <b-col>
            <b-input-group>
                <b-input-group-prepend>
                    <b-form-select
                        :id="filename + '-lesson-resource'"
                        class="lesson-resource-type-select"
                        variant="primary"
                        :options="resourceTypeOptions"
                        :state="getBootstrapFormInputState(vuelidateObject.resourceType)"
                        :value="resourceType"
                        @input="$emit('update:resourceType', $event)"
                    />
                </b-input-group-prepend>
                <b-form-input
                    :id="filename + '-name'"
                    type="text"
                    :state="getBootstrapFormInputState(vuelidateObject.filename)"
                    :value="filename"
                    @input="$emit('update:filename', $event)"
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

    export default {
        props: {
            filename: {
                type: String,
                default: "",
            },
            resourceType: {
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
                resourceTypeOptions: [
                    { value: null, text: ""},
                    { value: 1, text: "Student Handout"},
                    { value: 2, text: "Teacher Reference"},
                    { value: 3, text: "Slides"},
                    { value: 4, text: "Code"},
                    { value: 5, text: "Schematic"},
                    { value: 0, text: "Other"},
                ],
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