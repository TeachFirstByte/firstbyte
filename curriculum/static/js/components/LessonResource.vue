<template>
    <b-row fluid="mb-2">
        <b-col>
            <b-form-select
                :id="filename + '-lesson-resource'"
                v-model="$v.resourceType.$model"
                :options="resourceTypeOptions"
                :state="getBootstrapFormInputState($v.resourceType)"
            />
            <b-input-group>
                <b-form-input
                    :id="filename + '-name'"
                    v-model="$v.filename.$model"
                    type="text"
                    :state="getBootstrapFormInputState($v.filename)"
                />
                <b-input-group-append>
                    <b-button
                        class="remove-btn"
                        variant="danger"
                        aria-label="Remove"
                        @click="onRemove"
                    >
                        <span aria-hidden="true">&times;</span>
                    </b-button>
                </b-input-group-append>
            </b-input-group>
        </b-col>
    </b-row>
</template>
<script>

    import { validationMixin } from 'vuelidate';
    import { required } from 'vuelidate/lib/validators';

    import { getBootstrapFormInputState } from '../componentUtil.js';

    export default {
        mixins: [validationMixin],
        props: {
            filename: {
                type: String,
                default: ""
            },
            onRemove: {
                type: Function,
                required: true
            }
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
                resourceType: null,

                lessonResourceName: this.filename,

                getBootstrapFormInputState
            };
        },
        validations: {
            filename: {
                required
            },
            resourceType: {
                required
            }
        },

        mounted() {
            if (this.filename) {
                this.$v.filename.$touch();
            }
        }

    };
</script>
<style lang="scss" scoped>
    .remove-btn {
        padding: 0 6px;
    }

</style>