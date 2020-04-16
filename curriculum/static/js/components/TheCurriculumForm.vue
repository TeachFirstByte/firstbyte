<template>
    <b-container class="my-5">
        <b-row>
            <b-col lg>
                <h4>Curriculum Information</h4>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Title:"
                            label-for="title-input"
                            :invalid-feedback="getInvalidFeedback($v.title)"
                            :state="getBootstrapFormInputState($v.title)"
                        >
                            <b-form-input
                                id="title-input"
                                v-model="$v.title.$model"
                                type="text"
                                :state="getBootstrapFormInputState($v.title)"
                            />
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Summary:"
                            label-for="summary-input"
                            :invalid-feedback="getInvalidFeedback($v.summary)"
                            :state="getBootstrapFormInputState($v.summary)"
                        >
                            <b-form-textarea
                                id="summary-input"
                                v-model="$v.summary.$model"
                                :state="getBootstrapFormInputState($v.summary)"
                            />
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Grade Level:"
                            label-for="grade-level-input"
                            :invalid-feedback="getInvalidFeedback($v.gradeLevel)"
                            :state="getBootstrapFormInputState($v.gradeLevel)"
                        >
                            <b-form-select
                                id="grade-level-input"
                                v-model="$v.gradeLevel.$model"
                                :options="gradeLevelOptions"
                                :state="getBootstrapFormInputState($v.gradeLevel)"
                            />
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Num Classes:"
                            label-for="num-classes-input"
                            :invalid-feedback="getInvalidFeedback($v.numClasses)"
                            :state="getBootstrapFormInputState($v.numClasses)"
                        >
                            <b-form-input
                                id="num-classes-input"
                                v-model="$v.numClasses.$model"
                                type="number"
                                min="1"
                                :state="getBootstrapFormInputState($v.numClasses)"
                            />
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Single Class Time:"
                            label-for="single-class-time-input"
                            :invalid-feedback="getInvalidFeedback($v.singleClassTime)"
                            :state="getBootstrapFormInputState($v.singleClassTime)"
                        >
                            <b-form-select
                                id="single-class-time-input"
                                v-model="$v.singleClassTime.$model"
                                :options="durationOptions"
                                :state="getBootstrapFormInputState($v.singleClassTime)"
                            />
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Total Prep Time:"
                            label-for="total-prep-time-input"
                            :invalid-feedback="getInvalidFeedback($v.totalPrepTime)"
                            :state="getBootstrapFormInputState($v.totalPrepTime)"
                        >
                            <b-form-select
                                id="total-prep-time-input"
                                v-model="$v.totalPrepTime.$model"
                                :options="durationOptions"
                                :state="getBootstrapFormInputState($v.totalPrepTime)"
                            />
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Materials:"
                            label-for="materials-input"
                            :invalid-feedback="getInvalidFeedback($v.materials)"
                            :state="getBootstrapFormInputState($v.materials)"
                        >
                            <LineItemInput
                                id="materials-input"
                                :states="materialsBootstrapStates"
                                :value="materials"
                                @update:value="onMaterialsUpdate"
                                @touch="onMaterialsTouch"
                            />
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group>
                            <b-form-checkbox
                                id="web-only-input"
                                v-model="webOnly"
                            >
                                Web only
                            </b-form-checkbox>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group>
                            <b-form-checkbox
                                id="feedback-enabled-input"
                                v-model="feedbackEnabled"
                            >
                                Allow reviews
                            </b-form-checkbox>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group>
                            <b-form-checkbox
                                id="draft-input"
                                v-model="draft"
                            >
                                This a draft
                            </b-form-checkbox>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            invalid-feedback="You must license this work under CC BY-NC 4.0 to submit it for access on our website."
                            :state="getBootstrapFormInputState($v.agree)"
                        >
                            <b-form-checkbox
                                id="agree-input"
                                v-model="$v.agree.$model"
                                :state="getBootstrapFormInputState($v.agree)"
                            >
                                I am the sole author or I have permission to license this work under the CC BY-NC 4.0 License
                            </b-form-checkbox>
                        </b-form-group>
                    </b-col>
                </b-row>
            </b-col>
            <b-col
                lg
                class="d-flex flex-column"
            >
                <h4>Upload Supporting Files</h4>
                <DropArea class="flex-grow-1">
                    <template #fileForm="{ filename, onRemove }">
                        <LessonResource
                            :filename="filename"
                            :on-remove="onRemove"
                        />
                    </template>
                </DropArea>
            </b-col>
        </b-row>
        <p class="lesson-submission-warning">
            Please see our <a href="{% url 'faq' %}">FAQ</a> for more information.
        </p>
        <b-row class="w-100 text-center">
            <b-col class="text-center">
                <input
                    id="submit-lesson-plan"
                    type="submit"
                    class="btn btn-primary mt-3"
                    for="lesson-plan-form"
                    value="Upload Curriculum"
                    @click="onSubmit"
                >
            </b-col>
        </b-row>
    </b-container>
</template>
<script>
    import DropArea from './DropArea.vue';
    import LessonResource from './LessonResource.vue';
    import LineItemInput from './LineItemInput.vue';

    import { validationMixin } from 'vuelidate';
    import { required, minValue } from 'vuelidate/lib/validators';

    import { getBootstrapFormInputState } from '../componentUtil.js';

    export default {
        components: {
            DropArea,
            LessonResource,
            LineItemInput
        },
        mixins: [validationMixin],
        data() {
            return {
                title: "",
                summary: "",
                gradeLevel: null,
                gradeLevelOptions: [
                    { value: null, text: "" },
                    { value: "ES", text: "Elementary School" },
                    { value: "MS", text: "Middle School" },
                    { value: "HS", text: "High School" },
                    { value: "U", text: "Post-secondary" },
                ],
                numClasses: null,
                totalPrepTime: null,
                singleClassTime: null,
                durationOptions: [
                    { value: null, text: ''},
                    { value: '0:00', text: '0:00' },
                    { value: '0:15', text: '0:15' },
                    { value: '0:30', text: '0:30' },
                    { value: '0:45', text: '0:45' },
                    { value: '1:00', text: '1:00' },
                    { value: '1:15', text: '1:15' },
                    { value: '1:30', text: '1:30' },
                    { value: '1:45', text: '1:45' },
                    { value: '2:00', text: '2:00' },
                    { value: '2:15', text: '2:15' },
                    { value: '2:30', text: '2:30' },
                    { value: '2:45', text: '2:45' },
                    { value: '3:00', text: '3:00' },
                    { value: '3:15', text: '3:15' },
                    { value: '3:30', text: '3:30' },
                    { value: '3:45', text: '3:45' },
                    { value: '4:00', text: '4:00' },
                    { value: '4:15', text: '4:15' },
                    { value: '4:30', text: '4:30' },
                    { value: '4:45', text: '4:45' },
                    { value: '5:00', text: '5:00' },
                    { value: '5:15', text: '5:15' },
                    { value: '5:30', text: '5:30' },
                    { value: '5:45', text: '5:45' },
                    { value: '6:00', text: '6:00' },
                ],
                materials: [""],
                webOnly: false,
                feedbackEnabled: false,
                draft: false,
                agree: false,

                getBootstrapFormInputState,
            };
        },
        computed: {
            materialsBootstrapStates() {
                return this.materials.map((_, index) => {
                    return getBootstrapFormInputState(this.$v.materials.$each[index]);
                });
            }
        },
        methods: {
            getInvalidFeedback(vuelidateObject) {
                return !vuelidateObject.required ? "This field is required" : "";
            },
            onMaterialsUpdate(newArray) {
                this.materials = newArray;
            },
            onMaterialsTouch(index) {
                this.$v.materials.$each[index].$touch();
            },
            onSubmit(_) {
                this.$v.$touch();
            }
        },
        validations: {
            title: {
                required,
            },
            summary: {
                required,
            },
            gradeLevel: {
                required,
            },
            numClasses: {
                required,
                minValue: minValue(1)
            },
            totalPrepTime: {
                required,
            },
            singleClassTime: {
                required,
            },
            materials: {
                required,
                $each: {
                    required,
                }
            },
            agree: {
                mustAgree: (value) => value
            },
        },
    };
</script>
<style lang="scss">
    b-form-select {
        appearance: none;
    }
</style>