<template>
    <div>
        <span
            class="mb-2"
            style="user-select: none;"
            @click="$refs.fileInput.click()"
        >
            Attach materials by dragging &amp; dropping or clicking in the box below.
        </span>
        <div
            :class="{'droparea--pending-drop': pendingDrop}"
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
            <b-form-group
                v-for="file in files"
                :key="file.name"
            >
                <slot
                    name="fileForm"
                    :filename="file.name"
                    :onRemove="buildOnRemoveCallback(file)"
                />
            </b-form-group>
        </div>
    </div>
</template>
<script>
    export default {
        data() {
            return {
                pendingDrop: false,
                files: []
            };
        },
        methods: {
            buildOnRemoveCallback(file) {
                return () => {
                    this.files.splice(this.files.indexOf(file), 1);
                };
            },
            onFileUpload(event) {
                let files = event.currentTarget.files;
                for(let index = 0; index < files.length; ++index) {
                    let file = files[index];
                    this.files.push(file);
                }
            },
            onDropHandler(event) {
                if (event.dataTransfer.items) {
                    // Use DataTransferItemList interface to access the file(s)
                    for (let i = 0; i < event.dataTransfer.items.length; i++) {
                        // If dropped items aren't files, reject them
                        if (event.dataTransfer.items[i].kind === 'file') {
                            let file = event.dataTransfer.items[i].getAsFile();
                            this.files.push(file);
                        }
                    }
                    event.dataTransfer.items.clear();

                } else {
                    // Use DataTransfer interface to access the file(s)
                    for (let i = 0; i < event.dataTransfer.files.length; i++) {
                        let file = event.dataTransfer.files[i];
                        this.files.push(file);
                    }

                    event.dataTransfer.clearData();
                }
                // We've handled the drag
                this.onDragExitHandler();
            },
            onDragEnterHandler() {
                this.pendingDrop = true;
            },
            onDragExitHandler() {
                this.pendingDrop = false;
            }
        },
    };
</script>
<style lang="scss" scoped>
    .droparea {
        height: 100%;
        min-height: 10em;
        border: 1px dashed #cacaca;
    }

    .droparea--pending-drop {
        background-color: lightskyblue;
    }
</style>