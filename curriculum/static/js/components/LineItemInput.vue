<template>
    <div>
        <div
            v-for="(item, index) in $v.items.$each.$iter"
            :key="index"
            class="d-flex mb-2"
        >
            <input
                ref="itemInputs"
                class="flex-grow-1 mr-1 form-control"
                :class="{'is-valid': isValid(item), 'is-invalid': isInvalid(item)}"
                :value="item.$model"
                @input="onInput(index, $event.target.value)"
                @keyup.enter="insertItemAndFocus(index)"
            >
            <font-awesome-icon
                v-if="index == items.length - 1"
                class="text-secondary align-self-center"
                :icon="['fas', 'plus-circle']"
                size="lg"
                @click="addItem"
            />
            <font-awesome-icon
                v-else
                class="text-danger align-self-center"
                :icon="['fas', 'minus-circle']"
                size="lg"
                @click="removeItemAtIndex(index)"
            />
        </div>
    </div>
</template>
<script>
    import { validationMixin } from 'vuelidate';
    import { required } from 'vuelidate/lib/validators';

    export default {
        mixins: [validationMixin],
        data() {
            return {
                items: [""],
            };
        },
        validations: {
            items: {
                required,
                $each: {
                    required
                }
            }
        },
        methods: {
            addItem() {
                this.items.push("");
            },
            insertItemAndFocus(index) {
                let start = parseInt(index) + 1;
                this.items.splice(start, 0, "");
                this.$nextTick().then(() => {
                    this.$refs.itemInputs[start].focus();
                });

            },
            removeItemAtIndex(index) {
                this.items.splice(index, 1);
            },
            onInput(index, value) {
                this.$set(this.items, index, value);
                this.$v.items.$each[index].$touch();
            },
            isValid(item) {
                return item.$dirty && !item.$error;
            },
            isInvalid(item) {
                return item.$dirty && item.$error;
            }
        }
    };
</script>
<style lang="scss" scoped>
</style>