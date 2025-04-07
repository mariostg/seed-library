window.onload = function () {
    slideFromBloomPeriod();
    slideToBloomPeriod();

    slideFromPlantHeight();
    slideToPlantHeight();

    slideFromPlantWidth();
    slideToPlantWidth();
};

let sliderFromPlantHeight = document.getElementById("sliderFromPlantHeight");
let sliderToPlantHeight = document.getElementById("sliderToPlantHeight");
let displayValOnePlantHeight = document.getElementById("rangeFromPlantHeight");
let displayValTwoPlantHeight = document.getElementById("rangeToPlantHeight");
let minGapPlantHeight = 0;
let sliderTrackPlantHeight = document.querySelector(".slider-track-plant-height");
let sliderMaxValuePlantHeight = document.getElementById("sliderFromPlantHeight").max;

let sliderFromPlantWidth = document.getElementById("sliderFromPlantWidth");
let sliderToPlantWidth = document.getElementById("sliderToPlantWidth");
let displayValOnePlantWidth = document.getElementById("rangeFromPlantWidth");
let displayValTwoPlantWidth = document.getElementById("rangeToPlantWidth");
let minGapPlantWidth = 0;
let sliderTrackPlantWidth = document.querySelector(".slider-track-plant-width");
let sliderMaxValuePlantWidth = document.getElementById("sliderFromPlantWidth").max;

let sliderFromBloomPeriod = document.getElementById("sliderFromBloomPeriod");
let sliderToBloomPeriod = document.getElementById("sliderToBloomPeriod");
let displayValOneBloomPeriod = document.getElementById("rangeFromBloomPeriod");
let displayValTwoBloomPeriod = document.getElementById("rangeToBloomPeriod");
let minGapBloomPeriod = 0;
let sliderTrackBloomPeriod = document.querySelector(".slider-track-bloom-period");
let sliderMaxValueBloomPeriod = document.getElementById("sliderFromBloomPeriod").max;

function updateSliderDisplay(slider, displayElement, value) {
    slider.value = value;
    displayElement.textContent = value;
}
const monthMap = {
    0: "January",
    1: "February",
    2: "March",
    3: "April",
    4: "May",
    5: "June",
    6: "July",
    7: "August",
    8: "September",
    9: "October",
    10: "November",
    11: "December",
};
function slideFromBloomPeriod() {
    try {
        // Convert values to numbers once
        let sliderFromValue = parseInt(sliderFromBloomPeriod.value) || 0;
        const sliderTwoValue = parseInt(sliderToBloomPeriod.value) || 0;
        console.log("sliderFromValue", sliderFromValue);
        console.log("sliderTwoValue", sliderTwoValue);
        // Ensure minimum gap and bounds
        if (sliderTwoValue - sliderFromValue <= minGapBloomPeriod) {
            const newValue = Math.max(0, sliderTwoValue - minGapBloomPeriod);
            console.log("newValue", newValue);
            // sliderFromValue = newValue;
            updateSliderDisplay(sliderFromBloomPeriod, displayValOneBloomPeriod, monthMap[newValue]);
        } else {
            displayValOneBloomPeriod.textContent = monthMap[sliderFromValue];
        }

        // Update slider colors
        fillColor(
            sliderFromBloomPeriod,
            sliderToBloomPeriod,
            sliderTrackBloomPeriod,
            sliderMaxValueBloomPeriod
        );
    } catch (error) {
        console.error("Error in slideFromBloomPeriod:", error);
    }
}

function slideToBloomPeriod() {
    try {
        // Convert values to numbers once
        const sliderFormValue = parseInt(sliderFromBloomPeriod.value) || 0;
        const sliderTwoValue = parseInt(sliderToBloomPeriod.value) || 0;

        // Ensure minimum gap and bounds
        if (sliderTwoValue - sliderFormValue <= minGapBloomPeriod) {
            const newValue = Math.min(sliderFormValue + minGapBloomPeriod, sliderMaxValueBloomPeriod);
            updateSliderDisplay(sliderToBloomPeriod, displayValTwoBloomPeriod, monthMap[newValue]);
        } else {
            displayValTwoBloomPeriod.textContent = monthMap[sliderTwoValue];
        }

        // Update slider colors
        fillColor(
            sliderFromBloomPeriod,
            sliderToBloomPeriod,
            sliderTrackBloomPeriod,
            sliderMaxValueBloomPeriod
        );
    } catch (error) {
        console.error("Error in slideToBloomPeriod:", error);
    }
}

function slideFromPlantHeight() {
    try {
        // Convert values to numbers once
        const sliderFormValue = parseInt(sliderFromPlantHeight.value) || 0;
        const sliderTwoValue = parseInt(sliderToPlantHeight.value) || 0;

        // Ensure minimum gap and bounds
        if (sliderTwoValue - sliderFormValue <= minGapPlantHeight) {
            const newValue = Math.max(0, sliderTwoValue - minGapPlantHeight);
            updateSliderDisplay(sliderFromPlantHeight, displayValOnePlantHeight, newValue);
        } else {
            displayValOnePlantHeight.textContent = sliderFormValue;
        }

        // Update slider colors
        fillColor(
            sliderFromPlantHeight,
            sliderToPlantHeight,
            sliderTrackPlantHeight,
            sliderMaxValuePlantHeight
        );
    } catch (error) {
        console.error("Error in slideFromPlantHeight:", error);
    }
}

function slideToPlantHeight() {
    try {
        // Convert values to numbers once
        const valueOne = parseInt(sliderFromPlantHeight.value) || 0;
        const valueTwo = parseInt(sliderToPlantHeight.value) || 0;

        // Ensure minimum gap and bounds
        if (valueTwo - valueOne <= minGapPlantHeight) {
            const newValue = Math.min(valueOne + minGapPlantHeight, sliderMaxValuePlantHeight);
            updateSliderDisplay(sliderToPlantHeight, displayValTwoPlantHeight, newValue);
        } else {
            displayValTwoPlantHeight.textContent = valueTwo;
        }

        // Update slider colors
        fillColor(
            sliderFromPlantHeight,
            sliderToPlantHeight,
            sliderTrackPlantHeight,
            sliderMaxValuePlantHeight
        );
    } catch (error) {
        console.error("Error in slideToPlantHeight:", error);
    }
}

function fillColor(sliderFrom, sliderTo, sliderTrack, sliderMaxValue) {
    const TRACK_COLOR = "#dadae5";
    const ACTIVE_COLOR = "#3264fe";

    // Ensure values are numbers and within bounds
    const value1 = Math.max(0, Math.min(parseInt(sliderFrom.value), sliderMaxValue));
    const value2 = Math.max(0, Math.min(parseInt(sliderTo.value), sliderMaxValue));

    // Calculate percentages
    const percent1 = (value1 / sliderMaxValue) * 100;
    const percent2 = (value2 / sliderMaxValue) * 100;

    // Apply gradient
    sliderTrack.style.background = `linear-gradient(to right,
        ${TRACK_COLOR} ${percent1}%,
        ${ACTIVE_COLOR} ${percent1}%,
        ${ACTIVE_COLOR} ${percent2}%,
        ${TRACK_COLOR} ${percent2}%
    )`
        .replace(/\s+/g, " ")
        .trim();
}

function slideFromPlantWidth() {
    try {
        // Convert values to numbers once
        const sliderFormValue = parseInt(sliderFromPlantWidth.value) || 0;
        const sliderTwoValue = parseInt(sliderToPlantWidth.value) || 0;

        // Ensure minimum gap and bounds
        if (sliderTwoValue - sliderFormValue <= minGapPlantWidth) {
            const newValue = Math.max(0, sliderTwoValue - minGapPlantWidth);
            updateSliderDisplay(sliderFromPlantWidth, displayValOnePlantWidth, newValue);
        } else {
            displayValOnePlantWidth.textContent = sliderFormValue;
        }

        // Update slider colors
        fillColor(sliderFromPlantWidth, sliderToPlantWidth, sliderTrackPlantWidth, sliderMaxValuePlantWidth);
    } catch (error) {
        console.error("Error in slideFromPlantWidth:", error);
    }
}

function slideToPlantWidth() {
    try {
        // Convert values to numbers once
        const valueOne = parseInt(sliderFromPlantWidth.value) || 0;
        const valueTwo = parseInt(sliderToPlantWidth.value) || 0;

        // Ensure minimum gap and bounds
        if (valueTwo - valueOne <= minGapPlantWidth) {
            const newValue = Math.min(valueOne + minGapPlantWidth, sliderMaxValuePlantWidth);
            updateSliderDisplay(sliderToPlantWidth, displayValTwoPlantWidth, newValue);
        } else {
            displayValTwoPlantWidth.textContent = valueTwo;
        }

        // Update slider colors
        fillColor(sliderFromPlantWidth, sliderToPlantWidth, sliderTrackPlantWidth, sliderMaxValuePlantWidth);
    } catch (error) {
        console.error("Error in slideToPlantWidth:", error);
    }
}

function updateWinterSowingValue(value) {
    const values = ["NA", "10 days", "30 days", "60 days", "90 days", "120 days", "2 years"];
    document.getElementById("winter-sowing-value").textContent = values[value];
}

function updateHarvestingPeriodStart(value) {
    const values = [
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
        "January",
        "February",
        "March",
    ];

    document.getElementById("harvesting-period-start-value").textContent = values[value];
}
