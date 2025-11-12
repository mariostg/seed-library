function toggleNextSibling(event) {
  current_element = event.target;
  const toggleMe = current_element.nextElementSibling;
  toggleMe.classList.toggle("collapsed");
  current_element.classList.toggle("expander");
  current_element.classList.toggle("collapser");
}
function toggleFilterWrapper() {
  const filterWrapper = document.getElementById("filter-wrapper");
  const buttonText = document.querySelector("#aside-toggler button");
  if (filterWrapper.style.display === "none") {
    filterWrapper.style.display = "flex";
    buttonText.innerHTML = "Hide Filters";
  } else {
    filterWrapper.style.display = "none";
    buttonText.innerHTML = "Show Filters";
  }
}

// a function that set style.display to none of filter-wrapper on page load if window.innerWidth < 768px
function setFilterWrapperDisplay() {
  const filterWrapper = document.getElementById("filter-wrapper");
  if (window.innerWidth < 768) {
    filterWrapper.style.display = "none";
    const buttonText = document.querySelector("#aside-toggler button");
    buttonText.innerHTML = "Show Filters";
  }
}

// call the function on page load
window.onload = setFilterWrapperDisplay;

// call the function on window resize
window.onresize = setFilterWrapperDisplay;
