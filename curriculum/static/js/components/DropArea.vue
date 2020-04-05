<template>
    <div>
        <span
            class="mb-3"
            style="user-select: none;"
            @click="$refs.fileInput.click()"
        >
            Attach materials by dragging &amp; dropping or clicking in the box below.
        </span>
        <div
            :class="{'droparea--pending-drop': pendingDrop}"
            class="droparea"
            @click.self="$refs.fileInput.click()"
            @drop="onDropHandler"
            @dragover="onDragOverHandler"
            @dragenter="onDragEnterHandler"
            @dragleave="onDragExitHandler"
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
                event.preventDefault();

                let originalEvent = event.originalEvent;

                if (originalEvent.dataTransfer.items) {
                    // Use DataTransferItemList interface to access the file(s)
                    for (let i = 0; i < originalEvent.dataTransfer.items.length; i++) {
                        // If dropped items aren't files, reject them
                        if (originalEvent.dataTransfer.items[i].kind === 'file') {
                            let file = originalEvent.dataTransfer.items[i].getAsFile();
                            this.files.push(file);
                        }
                    }
                    originalEvent.dataTransfer.items.clear();

                } else {
                    // Use DataTransfer interface to access the file(s)
                    for (let i = 0; i < originalEvent.dataTransfer.files.length; i++) {
                        let file = originalEvent.dataTransfer.files[i];
                        this.files.push(file);
                    }

                    originalEvent.dataTransfer.clearData();
                }
                // We've handled the drag
                this.onDragExitHandler();
            },
            onDragOverHandler(event) {
                event.preventDefault();
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