<template>
    <div>
        <draggable
            v-model="draggableValueModel"
            handle=".grip-handle"
        >
            <div
                v-for="(lineItem, index) in value"
                :key="index"
                class="d-flex mb-2"
            >
                <div class="grip-handle text-dark pr-2 align-self-center">
                    <font-awesome-icon
                        class="my-auto"
                        :icon="['fas', 'align-justify']"
                        size="lg"
                    />
                </div>
                <b-input-group>
                    <input
                        ref="itemInputs"
                        class="item-input flex-grow-1 form-control"
                        :class="{'is-valid': isValidAtIndex(index), 'is-invalid': isInvalidAtIndex(index)}"
                        :value="lineItem.value"
                        @input="onInput(index, $event.target.value)"
                        @keyup.enter="onInsertAfterIndexAndFocus(index)"
                    >
                    <b-input-group-append>
                        <b-button
                            class="remove-btn"
                            variant="danger"
                            aria-label="Remove"
                            :disabled="value.length <= 1"
                            @click="onRemoveItemAtIndex(index)"
                        >
                            <span aria-hidden="true">&times;</span>
                        </b-button>
                    </b-input-group-append>
                </b-input-group>
            </div>
        </draggable>
    </div>
</template>
<script>
    import draggable from 'vuedraggable';

    export default {
        components: {
            draggable,
        },
        props: {
            value: {
                type: Array,
                required: true,
            },
            states: {
                type: Array,
                default: () => { return []; },
            },
        },
        data() {
            return {
                idCounter: 0
            };
        },
        computed: {
            draggableValueModel: {
                get: function() {
                    return this.value;
                },
                set: function(newValue) {
                    this.updateValue(newValue);
                },
            },
        },
        methods: {
            updateValue(newValue) {
                this.$emit('update:value', newValue);
            },
            updateValueWithResult(fn) {
                this.updateValue(fn(this.value.slice()));
            },
            makeNewItem(initialValue) {
                initialValue = initialValue || "";
                return {
                    id: ++this.idCounter,
                    value: initialValue,
                    state: null,
                };
            },
            onAppendNewItem() {
                this.updateValueWithResult((newValue) => {
                    newValue.push(this.makeNewItem());
                    return newValue;
                });
            },
            onRemoveItemAtIndex(index) {
                this.updateValueWithResult((newValue) => {
                    newValue.splice(index, 1);
                    return newValue;
                });
            },
            onInput(index, inputFieldValue) {
                this.updateValueWithResult((newValue) => {
                    newValue[index].value = inputFieldValue;
                    return newValue;
                });
                this.$emit('touch', parseInt(index));
            },
            onInsertAfterIndexAndFocus(index) {
                if (this.value[index].value === "") {
                    return;
                }
                this.updateValueWithResult((newValue) => {
                    const start = parseInt(index) + 1;
                    newValue.splice(start, 0, this.makeNewItem());

                    this.$nextTick().then(() => {
                        this.$refs.itemInputs[start].focus();
                    });

                    return newValue;
                });
            },

            isValidAtIndex(index) {
                return this.states[index] === true;
            },
            isInvalidAtIndex(index) {
                return this.states[index] === false;
            }
        }
    };
</script>
<style lang="scss" scoped>
</style>