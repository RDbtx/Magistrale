/**
 * Synchronizes the values between a range slider and a number input field.
 *
 * This function ensures that when the user adjusts the slider, the corresponding
 * number input field updates accordingly, and when the user types a value into
 * the number input field, the slider reflects that change. The function also enforces
 * a valid range for the number input between -100 and 100.
 *
 * @param {string} sliderId - The ID of the range input element to synchronize.
 * @param {string} inputId - The ID of the number input element to synchronize.
 */
function syncSliderAndNumber(sliderId, inputId) {
    let slider = document.getElementById(sliderId);
    let input = document.getElementById(inputId);


    slider.addEventListener('input', function () {
        input.value = this.value;
    });

    input.addEventListener('input', function () {
        if (this.value < -100) this.value = -100;
        if (this.value > 100) this.value = 100;
        slider.value = this.value;
    });
}


syncSliderAndNumber('colorRange', 'colorValue');
syncSliderAndNumber('brightnessRange', 'brightnessValue');
syncSliderAndNumber('contrastRange', 'contrastValue');
syncSliderAndNumber('sharpnessRange', 'sharpnessValue');
