<template>
    <div class="d-flex align-items-center justify-content-start">
        <b-form-group
            class="flex-fill mr-4"
            label="Hours"
            label-size="sm"
            label-for="duration-input__hours"
            :state="state"
        >
            <b-form-input
                id="duration-input__hours"
                class="duration-input__input"
                aria-label="Hours"
                type="number"
                :number="true"
                :min="minHours"
                :max="maxHours"
                :step="hourStep"
                :value="hours"
                :state="state"
                @update="updateHours"
            />
        </b-form-group>
        <b-form-group
            class="flex-fill"
            label="Minutes"
            label-size="sm"
            label-for="duration-input__minutes"
            :state="state"
        >
            <b-form-input
                id="duration-input__minutes"
                class="duration-input__input"
                aria-label="Minutes"
                type="number"
                :number="true"
                :min="minMinutes"
                :max="maxMinutes"
                :step="minuteStep"
                :value="minutes"
                :state="state"
                @update="updateMinutes"
            />
        </b-form-group>
    </div>
</template>
<script>

    import { mod } from '../componentUtil.js';

    const MIN_MINUTES = 0;
    const NUM_MINUTES_IN_HOUR = 60;

    export default {
        props: {
            value: {
                default: "00:00:00",
                type: String,
            },
            minHours: {
                default: 0,
                type: Number,
            },
            maxHours: {
                default: null,
                type: Number,
            },
            hourStep: {
                default: null,
                type: Number,
            },
            minuteStep: {
                default: null,
                type: Number,
            },
            state: {
                default: null,
                type: Boolean,
            },
        },
        data() {
            const negativeSentinelValue = MIN_MINUTES - this.minuteStep;
            return {
                hours: 0,
                minutes: 0,
                minMinutes: negativeSentinelValue,
                maxMinutes: NUM_MINUTES_IN_HOUR,
            };
        },
        computed: {
            formattedDuration() {
                const hoursPadded = this.hours.toString().padStart(2, '0');
                const minutesPadded = this.minutes.toString().padStart(2, '0');
                return `00:${hoursPadded}:${minutesPadded}`;
            },
        },
        watch: {
            value: {
                immediate: true,
                handler: function(newValue) {
                    if (!newValue) {
                        return;
                    }
                    const durationParts = newValue.split(':');
                    this.hours = parseInt(durationParts[1]);
                    this.minutes = parseInt(durationParts[2]);
                },
            },
        },
        methods: {
            updateValue() {
                this.$emit('input', this.formattedDuration);
            },
            updateHours(newHours) {
                this.hours = newHours;
                this.updateValue();
            },
            updateMinutes(newMinutes) {
                if (newMinutes === NUM_MINUTES_IN_HOUR && this.hours < this.maxHours) {
                    this.hours += 1;
                    this.minutes = 0;
                } else if (newMinutes === this.minMinutes && this.minHours < this.hours) {
                    this.hours -= 1;
                    this.minutes = 45;
                } else {
                    this.minutes = mod(newMinutes, NUM_MINUTES_IN_HOUR);
                }

                this.updateValue();
            },
        },
    };
</script>