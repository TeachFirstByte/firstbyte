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
                :step="minutesStep"
                :value="minutes"
                :state="state"
                @update="updateMinutes"
            />
        </b-form-group>
    </div>
</template>
<script>

    const NUM_MINUTES_IN_HOUR = 60;
    const OVERFLOW_MINUTES = NUM_MINUTES_IN_HOUR;

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
            minutesStep: {
                default: null,
                type: Number,
            },
            state: {
                default: null,
                type: Boolean,
            },
        },
        data() {
            return {
                hours: 0,
                minutes: 0,
            };
        },
        computed: {
            formattedDuration() {
                const hoursPadded = this.hours.toString().padStart(2, '0');
                const minutesPadded = this.minutes.toString().padStart(2, '0');
                return `${hoursPadded}:${minutesPadded}:00`;
            },
            underflowMinutes() {
                return -this.minutesStep;
            },
            minMinutes() {
                return this.minHours === this.hours ? 0 : this.underflowMinutes;
            },
            maxMinutes() {
                return this.maxHours === this.hours ? NUM_MINUTES_IN_HOUR - this.minutesStep : OVERFLOW_MINUTES;
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
                    this.hours = parseInt(durationParts[0]);
                    this.minutes = parseInt(durationParts[1]);
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
                if (newMinutes === OVERFLOW_MINUTES) {
                    this.hours += 1;
                    this.minutes = 0;
                } else if (newMinutes === this.underflowMinutes) {
                    this.hours -= 1;
                    this.minutes = 45;
                } else {
                    this.minutes = newMinutes;
                }

                this.updateValue();
            },
        },
    };
</script>