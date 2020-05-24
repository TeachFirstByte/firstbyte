
/**
 * Return the appropriate value for bootstrap form component state props
 *
 * @param vuelidateObject Vuelidate $v.field object.
 * @returns true, false, or null
 */
export function getBootstrapFormInputState(vuelidateObject) {
    if (vuelidateObject.$dirty) {
        return !vuelidateObject.$error;
    }
    return null;
}

export function mod(a, b) {
    return ((a % b) + b) % b;
}