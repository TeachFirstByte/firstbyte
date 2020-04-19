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
                            :invalid-feedback="getInvalidFeedback($v.formData.title)"
                            :state="getBootstrapFormInputState($v.formData.title)"
                        >
                            <b-form-input
                                id="title-input"
                                v-model="$v.formData.title.$model"
                                type="text"
                                :state="getBootstrapFormInputState($v.formData.title)"
                            />
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Summary:"
                            label-for="summary-input"
                            :invalid-feedback="getInvalidFeedback($v.formData.summary)"
                            :state="getBootstrapFormInputState($v.formData.summary)"
                        >
                            <b-form-textarea
                                id="summary-input"
                                v-model="$v.formData.summary.$model"
                                :state="getBootstrapFormInputState($v.formData.summary)"
                            />
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Grade Level:"
                            label-for="grade-level-input"
                            :invalid-feedback="getInvalidFeedback($v.formData.gradeLevel)"
                            :state="getBootstrapFormInputState($v.formData.gradeLevel)"
                        >
                            <b-form-select
                                id="grade-level-input"
                                v-model="$v.formData.gradeLevel.$model"
                                :options="gradeLevelOptions"
                                :state="getBootstrapFormInputState($v.formData.gradeLevel)"
                            />
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Num Classes:"
                            label-for="num-classes-input"
                            :invalid-feedback="getInvalidFeedback($v.formData.numClasses)"
                            :state="getBootstrapFormInputState($v.formData.numClasses)"
                        >
                            <b-form-input
                                id="num-classes-input"
                                v-model="$v.formData.numClasses.$model"
                                type="number"
                                min="1"
                                :state="getBootstrapFormInputState($v.formData.numClasses)"
                            />
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Single Class Time:"
                            label-for="single-class-time-input"
                            :invalid-feedback="getInvalidFeedback($v.formData.singleClassTime)"
                            :state="getBootstrapFormInputState($v.formData.singleClassTime)"
                        >
                            <b-form-select
                                id="single-class-time-input"
                                v-model="$v.formData.singleClassTime.$model"
                                :options="durationOptions"
                                :state="getBootstrapFormInputState($v.formData.singleClassTime)"
                            />
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Total Prep Time:"
                            label-for="total-prep-time-input"
                            :invalid-feedback="getInvalidFeedback($v.formData.totalPrepTime)"
                            :state="getBootstrapFormInputState($v.formData.totalPrepTime)"
                        >
                            <b-form-select
                                id="total-prep-time-input"
                                v-model="$v.formData.totalPrepTime.$model"
                                :options="durationOptions"
                                :state="getBootstrapFormInputState($v.formData.totalPrepTime)"
                            />
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Materials:"
                            label-for="materials-input"
                            :invalid-feedback="getInvalidFeedback($v.formData.materials)"
                            :state="getBootstrapFormInputState($v.formData.materials)"
                        >
                            <LineItemInput
                                id="materials-input"
                                :states="materialsBootstrapStates"
                                :value.sync="formData.materials"
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
                                v-model="formData.webOnly"
                            >
                                Web only
                            </b-form-checkbox>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group>
                            <b-form-checkbox
                                id="feedback-enabled-input"
                                v-model="formData.feedbackEnabled"
                            >
                                Allow reviews
                            </b-form-checkbox>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group>
                            <b-form-checkbox
                                id="draft-input"
                                v-model="formData.draft"
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
                            :state="getBootstrapFormInputState($v.formData.agree)"
                        >
                            <b-form-checkbox
                                id="agree-input"
                                v-model="$v.formData.agree.$model"
                                :state="getBootstrapFormInputState($v.formData.agree)"
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
                <span class="mb-2">
                    Attach materials by dragging &amp; dropping or clicking in the box below.
                </span>
                <LessonResourceList
                    :lesson-resources.sync="formData.lessonResources"
                    :vuelidate-object="$v.formData.lessonResources"
                />
            </b-col>
        </b-row>
        <p class="lesson-submission-warning">
            Please see our <a href="{% url 'faq' %}">FAQ</a> for more information.
        </p>
        <b-row class="w-100 text-center">
            <b-col class="text-center">
                <b-button
                    variant="primary"
                    class="mt-3"
                    @click="onSubmit"
                >
                    <b-spinner
                        v-if="submissionLoading"
                        small
                        variant="light"
                    />
                    Upload Curriculum
                </b-button>
            </b-col>
        </b-row>
    </b-container>
</template>
<script>
    import LessonResourceList from './LessonResourceList.vue';
    import LineItemInput from './LineItemInput.vue';

    import { validationMixin } from 'vuelidate';
    import { required, minValue } from 'vuelidate/lib/validators';

    import { getBootstrapFormInputState } from '../componentUtil.js';

    export const GRADE_LEVEL_OPTIONS = [
        { value: null, text: "" },
        { value: "ES", text: "Elementary School" },
        { value: "MS", text: "Middle School" },
        { value: "HS", text: "High School" },
        { value: "U", text: "Post-secondary" },
    ];
    export const DURATION_OPTIONS = [
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
    ];

    function submitCurriculum(client, formData, updatingCurriculumId) {
        let lessonPlanFormData = new FormData();

        lessonPlanFormData.append('title', formData.title);
        lessonPlanFormData.append('grade_level', formData.gradeLevel);
        lessonPlanFormData.append('num_classes', formData.numClasses);
        lessonPlanFormData.append('summary', formData.summary);
        lessonPlanFormData.append('total_prep_time', formData.totalPrepTime);
        lessonPlanFormData.append('single_class_time', formData.singleClassTime);
        lessonPlanFormData.append('materials', JSON.stringify(formData.materials.map((it) => { return it.value; })));
        lessonPlanFormData.append('web_only', formData.webOnly);
        lessonPlanFormData.append('feedback_enabled', formData.feedbackEnabled);
        lessonPlanFormData.append('draft', formData.draft);

        lessonPlanFormData.append('agree', formData.agree);
        lessonPlanFormData.append('jsonResponse', true);

        let resourceIds = [];
        let resourceTypes = [];
        let filenames = [];
        let files = [];

        formData.lessonResources.forEach((resource) => {
            // TODO: If this is a new lessonplan put it at the end
            if (resource.resourceId) {
                resourceIds.push(resource.resourceId);
            }
            resourceTypes.push(resource.resourceType);
            filenames.push(resource.filename);
            files.push(resource.file);
        });

        lessonPlanFormData.append('resource_ids', JSON.stringify(resourceIds));
        lessonPlanFormData.append('filetypes', JSON.stringify(resourceTypes));
        lessonPlanFormData.append('filenames', JSON.stringify(filenames));

        files.forEach((file) => {
            lessonPlanFormData.append('files[]', file);
        });

        let submissionPromise;
        if (updatingCurriculumId) {
            submissionPromise = client.updateLessonPlan(lessonPlanFormData, updatingCurriculumId);
        } else {
            submissionPromise = client.submitLessonPlan(lessonPlanFormData);
        }

        submissionPromise.then(function(response) {
            window.location.href = '/lesson-plans/' + response.id;
        }).catch(function(error) {
            console.error(error);
        });
    }

    function retrieveExistingLessonResources(util) {
        let lessonResources = [];

        if(util.updatingCurriculumId) {
            util.client.getLessonPlan(util.updatingCurriculumId).then(function(lessonplan) {
                for (let i = 0; i < lessonplan.resources.length; ++i) {
                    let resource = lessonplan.resources[i];
                    // TODO: Make sure the ID we assign here doesn't interfere with added lesson resources
                    lessonResources.push({
                        id: resource.id,
                        resourceId: resource.id,
                        file: null,
                        filename: resource.name,
                        resourceType: resource.semantic_type,
                    });
                }
            }).catch(function(err) {
                console.log(err);
            });
        }

        return lessonResources;
    }

    export default {
        components: {
            LineItemInput,
            LessonResourceList,
        },
        mixins: [validationMixin],
        data() {
            return {
                gradeLevelOptions: GRADE_LEVEL_OPTIONS,
                durationOptions: DURATION_OPTIONS,
                formData: {
                    title: "",
                    summary: "",
                    gradeLevel: null,
                    numClasses: null,
                    totalPrepTime: null,
                    singleClassTime: null,
                    materials: [{id: 0, value: ""}],
                    webOnly: false,
                    feedbackEnabled: false,
                    draft: false,
                    agree: false,
                    lessonResources: [],
                },
                submissionLoading: false,
                getBootstrapFormInputState,
            };
        },
        computed: {
            materialsBootstrapStates() {
                return this.formData.materials.map((_, index) => {
                    return getBootstrapFormInputState(this.$v.formData.materials.$each[index]);
                });
            },
        },
        mounted() {
            this.formData.lessonResources = retrieveExistingLessonResources(this.$curriculumForm);
        },
        methods: {
            getInvalidFeedback(vuelidateObject) {
                return !vuelidateObject.required ? "This field is required" : "";
            },
            onMaterialsTouch(index) {
                this.$v.formData.materials.$each[index].$touch();
            },
            onSubmit(_) {
                this.$v.formData.$touch();
                if (!this.$v.formData.$anyError) {
                    submitCurriculum(this.$curriculumForm.client, this.formData, this.$curriculumForm.updatingCurriculumId);
                }
            },
        },
        validations: {
            formData: {
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
                    minValue: minValue(1),
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
                        $trackBy: "id",
                        value: {
                            required,
                        },
                    },
                },
                agree: {
                    mustAgree: (value) => value,
                },
                lessonResources: {
                    $each: {
                        $trackBy: "id",
                        filename: {
                            required,
                        },
                        resourceType: {
                            required,
                        },
                    },
                },
            },
        },
    };
</script>
<style lang="scss">
    b-form-select {
        appearance: none;
    }
</style>