window.onload = function () {
  slideFromBloomPeriod();
  slideToBloomPeriod();
};

let sliderFromBloomPeriod = document.getElementById("sliderFromBloomPeriod");
let sliderToBloomPeriod = document.getElementById("sliderToBloomPeriod");
let displayValOneBloomPeriod = document.getElementById("rangeFromBloomPeriod");
let displayValTwoBloomPeriod = document.getElementById("rangeToBloomPeriod");
let minGapBloomPeriod = 0;
let sliderTrackBloomPeriod = document.querySelector(
  ".slider-track-bloom-period"
);
let sliderMaxValueBloomPeriod = document.getElementById(
  "sliderFromBloomPeriod"
).max;

function updateSliderDisplay(slider, displayElement, value) {
  slider.value = value;
  displayElement.textContent = value;
}
const monthMap = {
  1: "January",
  2: "February",
  3: "March",
  4: "April",
  5: "May",
  6: "June",
  7: "July",
  8: "August",
  9: "September",
  10: "October",
  11: "November",
  12: "December",
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
      updateSliderDisplay(
        sliderFromBloomPeriod,
        displayValOneBloomPeriod,
        monthMap[newValue]
      );
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
      const newValue = Math.min(
        sliderFormValue + minGapBloomPeriod,
        sliderMaxValueBloomPeriod
      );
      updateSliderDisplay(
        sliderToBloomPeriod,
        displayValTwoBloomPeriod,
        monthMap[newValue]
      );
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

function fillColor(sliderFrom, sliderTo, sliderTrack, sliderMaxValue) {
  const TRACK_COLOR = "#dadae5";
  const ACTIVE_COLOR = "#3264fe";

  // Ensure values are numbers and within bounds
  const value1 = Math.max(
    0,
    Math.min(parseInt(sliderFrom.value), sliderMaxValue)
  );
  const value2 = Math.max(
    0,
    Math.min(parseInt(sliderTo.value), sliderMaxValue)
  );

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

function updateWinterSowingValue(value) {
  const values = [
    "NA",
    "10 days",
    "30 days",
    "60 days",
    "90 days",
    "120 days",
    "2 years",
  ];
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

  document.getElementById("harvesting-period-start-value").textContent =
    values[value];
}
