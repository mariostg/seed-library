function toggleHtmlBlock(toggleId) {
  current_element = event.target;
  current_element.classList.toggle("expanded");
  current_element.classList.toggle("collapser");
  const toggleMe = document.querySelector(toggleId);
  toggleMe.classList.toggle("collapsed");
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
