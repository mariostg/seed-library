(function () {
  toggler = document.querySelectorAll(".toggler");
  for (let t of toggler) {
    t.addEventListener("click", function () {
      set_availability(this);
    });
  }
})();

function set_availability(elem) {
  if (elem) {
    fetch("/toggle-availability/" + elem.dataset.pk, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // elem.children[2].innerHTML = data.availability;
        if (data.availability || data.availability == "True") {
          elem.classList.add("ok");
        } else {
          elem.classList.remove("ok");
        }
      });
  } else {
    console.log("NO PK");
  }
}
