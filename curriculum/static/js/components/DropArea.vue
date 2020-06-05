<template>
    <div
        :class="{'droparea--pending-drop': pendingDrop, 'droparea--highlight': highlight}"
        class="droparea"
        @click.self="$refs.fileInput.click()"
        @drop.prevent="onDropHandler"
        @dragenter="onDragEnterHandler"
        @dragleave="onDragExitHandler"
        @dragover.prevent
    >
        <input
            ref="fileInput"
            style="display: none;"
            type="file"
            multiple
            @change="onFileUpload"
        >
        <slot />
    </div>
</template>
<script>
    export default {
        props: {
            highlight: {
                type: Boolean,
                default: false,
            },
        },
        data() {
            return {
                pendingDrop: false,
            };
        },
        methods: {
            onFileUpload(event) {
                let newFiles = [];
                let files = event.currentTarget.files;
                for(let index = 0; index < files.length; ++index) {
                    let file = files[index];
                    newFiles.push(file);
                }
                this.$emit('newFiles', newFiles);
            },
            onDropHandler(event) {
                let newFiles = [];

                if (event.dataTransfer.items) {
                    // Use DataTransferItemList interface to access the file(s)
                    for (let i = 0; i < event.dataTransfer.items.length; i++) {
                        // If dropped items aren't files, reject them
                        if (event.dataTransfer.items[i].kind === 'file') {
                            let file = event.dataTransfer.items[i].getAsFile();
                            newFiles.push(file);
                        }
                    }
                    event.dataTransfer.items.clear();
                } else {
                    // Use DataTransfer interface to access the file(s)
                    for (let i = 0; i < event.dataTransfer.files.length; i++) {
                        let file = event.dataTransfer.files[i];
                        newFiles.push(file);
                    }

                    event.dataTransfer.clearData();
                }

                this.onDragExitHandler();
                this.$emit('newFiles', newFiles);
            },
            onDragEnterHandler() {
                this.pendingDrop = true;
            },
            onDragExitHandler() {
                this.pendingDrop = false;
            },
        },
    };
</script>
<style lang="scss" scoped>
    .droparea {
        min-height: 10em;
    }

    .droparea--highlight {
        border: 1px dashed #cacaca;
    }

    .droparea--pending-drop {
        background-color: lightskyblue;
    }
</style>