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

function resetFilter() {
  // Reset all filter inputs to their default values and delete the html inside the plant-cards class
  const filterForm = document.getElementById("filter-form");
  filterForm.reset();
}
