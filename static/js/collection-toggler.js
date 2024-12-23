(function () {
  const toggler = document.querySelectorAll(".toggler");
  for (let t of toggler) {
    t.addEventListener("click", function () {
      set_plant_ownwership(this);
    });
  }
})();

function set_plant_ownwership(elem) {
  const symbols = { No: "crossmark", Yes: "checkmark" };
  if (elem) {
    fetch("/user-plant-toggle/" + elem.dataset.pk, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // elem.innerHTML = data.isowner;
        elem.classList.remove(...Object.values(symbols));
        elem.classList.add(symbols[data.isowner]);
        console.log(data.isowner);
      });
  }
}
