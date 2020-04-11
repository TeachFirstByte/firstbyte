<template>
    <div>
        <div
            v-for="(lineItem, index) in value"
            :key="index"
            class="d-flex mb-2"
        >
            <input
                ref="itemInputs"
                class="flex-grow-1 mr-1 form-control"
                :class="{'is-valid': isValidAtIndex(index), 'is-invalid': isInvalidAtIndex(index)}"
                :value="lineItem"
                @input="onInput(index, $event.target.value)"
                @keyup.enter="onInsertAfterIndexAndFocus(index)"
            >
            <font-awesome-icon
                v-if="index == value.length - 1"
                class="text-secondary align-self-center"
                :icon="['fas', 'plus-circle']"
                size="lg"
                @click="onAppendNewItem"
            />
            <font-awesome-icon
                v-else
                class="text-danger align-self-center"
                :icon="['fas', 'minus-circle']"
                size="lg"
                @click="onRemoveItemAtIndex(index)"
            />
        </div>
    </div>
</template>
<script>
    export default {
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
        methods: {
            emitInputWithNewValue(method) {
                this.$emit('update', method(this.value.slice()));
            },
            onAppendNewItem() {
                this.emitInputWithNewValue((newValue) => {
                    newValue.push("");
                    return newValue;
                });
            },
            onRemoveItemAtIndex(index) {
                this.emitInputWithNewValue((newValue) => {
                    newValue.splice(index, 1);
                    return newValue;
                });
            },
            onInput(index, inputFieldValue) {
                this.emitInputWithNewValue((newValue) => {
                    newValue[index] = inputFieldValue;
                    return newValue;
                });
                this.$emit('touch', parseInt(index));
            },
            onInsertAfterIndexAndFocus(index) {
                this.emitInputWithNewValue((newValue) => {
                    const start = parseInt(index) + 1;
                    newValue.splice(start, 0, "");
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