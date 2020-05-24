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
                            <DurationInput
                                id="total-prep-time-input"
                                v-model="$v.formData.singleClassTime.$model"
                                :min-hours="0"
                                :minutes-step="15"
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
                            <DurationInput
                                id="total-prep-time-input"
                                v-model="$v.formData.totalPrepTime.$model"
                                :min-hours="0"
                                :minutes-step="15"
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
                <b-progress
                    v-if="submissionStatus.loading"
                    :value="submissionStatus.uploadProgress"
                    variant="primary"
                />
                <b-button
                    variant="primary"
                    class="mt-3"
                    @click="onSubmit"
                >
                    <b-spinner
                        v-if="submissionStatus.loading"
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
    import { validationMixin } from 'vuelidate';
    import { required, minValue, helpers } from 'vuelidate/lib/validators';
    import { cloneDeep, has, zip } from 'lodash';

    import LessonResourceList from './LessonResourceList.vue';
    import LineItemInput from './LineItemInput.vue';
    import DurationInput from './DurationInput.vue';

    import { getBootstrapFormInputState } from '../componentUtil.js';
    import { submitCurriculum, updateCurriculum, getCurriculum } from '../curriculumClient.js';

    export const GRADE_LEVEL_OPTIONS = [
        { value: null, text: "" },
        { value: "ES", text: "Elementary School" },
        { value: "MS", text: "Middle School" },
        { value: "HS", text: "High School" },
        { value: "U", text: "Post-secondary" },
    ];

    function submitCurriculumForm(formData, updatingCurriculumId, onUploadProgress) {
        let lessonPlanFormData = new FormData();

        lessonPlanFormData.append('title', formData.title);
        lessonPlanFormData.append('summary', formData.summary);
        lessonPlanFormData.append('gradeLevel', formData.gradeLevel);

        lessonPlanFormData.append('totalPrepTime', formData.totalPrepTime);
        lessonPlanFormData.append('numClasses', formData.numClasses);
        lessonPlanFormData.append('singleClassTime', formData.singleClassTime);

        lessonPlanFormData.append('webOnly', formData.webOnly);
        lessonPlanFormData.append('feedbackEnabled', formData.feedbackEnabled);
        lessonPlanFormData.append('draft', formData.draft);

        formData.materials.forEach((material) => {
            lessonPlanFormData.append('materialIds', material.id || "");
            lessonPlanFormData.append('materialNames', material.value);
        });

        formData.lessonResources.forEach((resource) => {
            lessonPlanFormData.append('lessonResourceIds', resource.id || "");
            lessonPlanFormData.append('lessonResourceTypes', resource.type);
            lessonPlanFormData.append('lessonResourceNames', resource.name);

            if (resource.file) {
                lessonPlanFormData.append('lessonResourceFiles', resource.file);
            }
        });

        let submissionPromise;
        if (updatingCurriculumId) {
            submissionPromise = updateCurriculum(updatingCurriculumId, {
                data: lessonPlanFormData,
                onUploadProgress: onUploadProgress,
            });
        } else {
            submissionPromise = submitCurriculum({
                data: lessonPlanFormData,
                onUploadProgress: onUploadProgress,
            });
        }

        return submissionPromise;
    }

    async function retrieveInitialFormData(existingCurriculumId) {
        if(existingCurriculumId) {
            const lessonPlan = await getCurriculum(existingCurriculumId);

            const buildMaterials = (materials) => {
                return materials.map((material) => {
                    return {
                        visualId: material.id,
                        id: material.id,
                        value: material.name,
                    };
                });
            };

            const buildResources = (resources) => {
                return resources.map((resource) => {
                    return {
                        visualId: resource.id,
                        id: resource.id,
                        name: resource.name,
                        type: resource.semanticType,
                    };
                });
            };

            const formData = {
                title: lessonPlan.title,
                summary: lessonPlan.summary,
                gradeLevel: lessonPlan.gradeLevel,
                totalPrepTime: lessonPlan.totalPrepTime,
                numClasses: lessonPlan.numClasses,
                singleClassTime: lessonPlan.singleClassTime,
                webOnly: lessonPlan.webOnly,
                feedbackEnabled: lessonPlan.feedbackEnabled,
                draft: lessonPlan.draft,
                lessonResources: buildResources(lessonPlan.resources),
            };

            const materials = buildMaterials(lessonPlan.materials);
            if (materials.length) {
                formData.materials = materials;
            }

            return formData;
        }

        return {};
    }

    function makeServerValidator(field) {
        return helpers.withParams(
            { type: 'serverValidationOk', field: field },
            function(currentFieldValue) {
                const status = this.submissionStatus;
                if (has(status.validationErrors, field) && has(status.submittedValues, field)
                    && status.submittedValues[field] === currentFieldValue) {
                    return !status.validationErrors[field].length;
                }
                return true;
            },
        );
    }
    function nonZeroDuration(duration) {
        return duration !== "00:00:00";
    }

    function durationInRange(min, max) {
        const minDurationParts = min.split(":").map((val) => parseInt(val));
        const maxDurationParts = max.split(":").map((val) => parseInt(val));
        return helpers.withParams(
            { type: 'durationInRange', min: min, max: max },
            function(duration) {
                const valueParts = duration.split(":").map((val) => parseInt(val));
                return zip(valueParts, minDurationParts, maxDurationParts).every((durationComponent) => {
                    return durationComponent[1] <= durationComponent[0] & durationComponent[0] <= durationComponent[2];
                });
            },
        );
    }

    export default {
        components: {
            LineItemInput,
            LessonResourceList,
            DurationInput,
        },
        mixins: [validationMixin],
        data() {
            return {
                gradeLevelOptions: GRADE_LEVEL_OPTIONS,
                formData: {
                    title: "",
                    summary: "",
                    gradeLevel: null,
                    numClasses: null,
                    totalPrepTime: null,
                    singleClassTime: null,
                    materials: [{visualId: 0, value: ""}],
                    webOnly: false,
                    feedbackEnabled: false,
                    draft: false,
                    agree: false,
                    lessonResources: [],
                },
                submissionStatus: {
                    loading: false,
                    uploadProgress: 0,
                    success: false,
                    submittedValues: {},
                    validationErrors: {},
                },

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
        async mounted() {
            this.onBeforeUnload = this.onBeforeUnload.bind(this);
            window.addEventListener('beforeunload', this.onBeforeUnload);

            const initialData = await retrieveInitialFormData(this.$curriculum.updatingCurriculumId);
            Object.assign(this.formData, initialData);
            this.$nextTick(() => this.$v.$reset());
        },
        unmounted() {
            window.removeEventListener('beforeunload', this.onBeforeUnload);
        },
        methods: {
            getInvalidFeedback(vuelidateObject) {
                if (!vuelidateObject.required || !vuelidateObject.nonZeroDuration) {
                    return "This field is required.";
                }

                if (!vuelidateObject.durationInRange) {
                    return "Duration is out of range.";
                }

                if (!vuelidateObject.serverValidationOk) {
                    return this.submissionStatus.validationErrors[vuelidateObject.$params.serverValidationOk.field].reduce(
                        (str, val) => str + val + '\n',
                        "",
                    );
                }
                return "";
            },
            onMaterialsTouch(index) {
                this.$v.formData.materials.$each[index].$touch();
            },
            onUploadProgress(event) {
                this.submissionStatus.uploadProgress = event.loaded / event.total * 100.0;
            },
            onBeforeUnload(event) {
                if (this.$v.$anyDirty && !this.submissionStatus.success) {
                    event.preventDefault();
                    event.returnValue = '';
                } else {
                    delete event['returnValue'];
                }
            },
            async onSubmit(_) {
                this.$v.formData.$touch();
                if (!this.$v.formData.$anyError) {
                    this.submissionStatus.loading = true;
                    this.submissionStatus.uploadProgress = 0;
                    try {
                        const response = await submitCurriculumForm(this.formData, this.$curriculum.updatingCurriculumId, this.onUploadProgress);
                        this.submissionStatus.success = true;
                        window.location.href = '/lesson-plans/' + response.data.id;
                    } catch (error) {
                        this.submissionStatus.loading = false;

                        const apiResponse = error.response;
                        if (apiResponse) {
                            this.submissionStatus.validationErrors = apiResponse.data;
                            this.submissionStatus.submittedValues = cloneDeep(this.formData);

                            this.$v.formData.$touch();
                            if (this.$v.formData.$anyError) {
                                this.$bvToast.toast('An error occurred. Please correct form errors.', {
                                    title: 'Submission Failure',
                                    autoHideDelay: 5000,
                                    appendToast: true,
                                    variant: 'danger',
                                });
                                return;
                            }
                        }

                        this.$bvToast.toast('An unknown error occurred. Please try again later.', {
                            title: 'Unknown Failure',
                            appendToast: true,
                            variant: 'danger',
                        });
                        console.error(error);
                    }
                }
            },
        },
        validations: {
            formData: {
                title: {
                    required,
                    serverValidationOk: makeServerValidator('title'),
                },
                summary: {
                    required,
                    serverValidationOk: makeServerValidator('summary'),
                },
                gradeLevel: {
                    required,
                    serverValidationOk: makeServerValidator('gradeLevel'),
                },
                numClasses: {
                    required,
                    minValue: minValue(1),
                    serverValidationOk: makeServerValidator('numClasses'),
                },
                totalPrepTime: {
                    required,
                    serverValidationOk: makeServerValidator('totalPrepTime'),
                    nonZeroDuration,
                    durationInRange: durationInRange("00:00:00", "00:06:45"),
                },
                singleClassTime: {
                    required,
                    serverValidationOk: makeServerValidator('singleClassTime'),
                    nonZeroDuration,
                    durationInRange: durationInRange("00:00:00", "00:06:45"),
                },
                materials: {
                    required,
                    serverValidationOk: makeServerValidator('materials'),
                    $each: {
                        $trackBy: "visualId",
                        value: {
                            required,
                        },
                    },
                },
                agree: {
                    mustAgree: (value) => value,
                    serverValidationOk: makeServerValidator('agree'),
                },
                lessonResources: {
                    serverValidationOk: makeServerValidator('lessonResources'),
                    $each: {
                        $trackBy: "visualId",
                        name: {
                            required,
                        },
                        type: {
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