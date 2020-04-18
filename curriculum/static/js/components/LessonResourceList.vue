<template>
    <DropArea
        class="flex-grow-1"
        :highlight="!lessonResources.length"
        @newFiles="addLessonResources"
    >
        <b-form-group
            v-for="(resource, index) in lessonResources"
            :key="resource.id"
        >
            <LessonResource
                :vuelidate-object="vuelidateObject.$each[index]"
                :filename.sync="vuelidateObject.$each[index].filename.$model"
                :resource-type.sync="vuelidateObject.$each[index].resourceType.$model"
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
                        id: ++this.idCounter,
                        file: file,
                        filename: file.name,
                        resourceType: null,
                    };
                });

                const oldLength = this.lessonResources.length;
                const numNewResources = newLessonResources.length;

                this.updateLessonResources([...this.lessonResources, ...newLessonResources]);

                this.$nextTick(() => {
                    [...Array(numNewResources).keys()].forEach((index) => {
                        this.vuelidateObject.$each[oldLength + index].filename.$touch();
                    });
                });

            },
            onRemove(resource) {
                this.updateLessonResources([...this.lessonResources].splice(this.lessonResources.indexOf(resource), 1));
            },
        },
    };
</script>
<style lang="scss" scoped>

</style>