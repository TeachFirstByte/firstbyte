<template>
    <DropArea
        class="flex-grow-1"
        :highlight="!lessonResources.length"
        @newFiles="addLessonResources"
    >
        <b-form-group
            v-for="(resource, index) in lessonResources"
            :key="resource.visualId"
        >
            <LessonResource
                :vuelidate-object="vuelidateObject.$each[index]"
                :name.sync="vuelidateObject.$each[index].name.$model"
                :type.sync="vuelidateObject.$each[index].type.$model"
                @onRemove="onRemove(resource)"
            />
        </b-form-group>
    </DropArea>
</template>
<script>
    import DropArea from './DropArea.vue';
    import LessonResource from './LessonResource.vue';

    export default {
        components: {
            DropArea,
            LessonResource,
        },
        props: {
            lessonResources: {
                type: Array,
                required: true,
            },
            vuelidateObject: {
                type: Object,
                default: () => { return {}; },
            },
        },
        data() {
            return {
                idCounter: 0,
            };
        },
        methods: {
            updateLessonResources(newArray) {
                this.$emit('update:lessonResources', newArray);
            },
            addLessonResources(newFiles) {
                const newLessonResources = newFiles.map((file) => {
                    return {
                        visualId: ++this.idCounter,
                        name: file.name,
                        type: null,
                        file: file,
                    };
                });

                const oldLength = this.lessonResources.length;
                const numNewResources = newLessonResources.length;

                this.updateLessonResources([...this.lessonResources, ...newLessonResources]);

                this.$nextTick(() => {
                    [...Array(numNewResources).keys()].forEach((index) => {
                        this.vuelidateObject.$each[oldLength + index].name.$touch();
                    });
                });

            },
            onRemove(resource) {
                let newArray = [...this.lessonResources];
                newArray.splice(this.lessonResources.indexOf(resource), 1);
                this.updateLessonResources(newArray);
            },
        },
    };
</script>
