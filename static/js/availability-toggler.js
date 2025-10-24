(function () {
  toggler = document.querySelectorAll(".toggler");
  for (let t of toggler) {
    t.addEventListener("click", function () {
      set_availability(this);
    });
  }

  is_active_toggler = document.querySelectorAll(".is-active-toggler");
  for (let t of is_active_toggler) {
    t.addEventListener("click", function () {
      set_is_active(this);
    });
  }
})();

is_seed_accepting_toggler = document.querySelectorAll(
  ".seed-accepting-toggler"
);
for (let t of is_seed_accepting_toggler) {
  t.addEventListener("click", function () {
    set_seed_accepting(this);
  });
}

is_plant_accepted_toggler = document.querySelectorAll(
  ".plant-accepted-toggler"
);
for (let t of is_plant_accepted_toggler) {
  t.addEventListener("click", function () {
    set_plant_accepted(this);
  });
}

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
        if (data.availability || data.availability == "True") {
          elem.classList.add("ok");
          elem.innerHTML = "&#x2713;";
        } else {
          elem.classList.remove("ok");
          elem.innerHTML = "✖️";
        }
      });
    console.log("PK", elem);
  } else {
    console.log("NO PK");
  }
}

function set_is_active(elem) {
  if (elem) {
    fetch("/toggle-is-active/" + elem.dataset.pk, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.is_active || data.is_active == "True") {
          elem.classList.add("ok");
          elem.innerHTML = "&#x2713;";
        } else {
          elem.classList.remove("ok");
          elem.innerHTML = "✖️";
        }
      });
  }
}

function set_seed_accepting(elem) {
  if (elem) {
    fetch("/toggle-seed-accepting/" + elem.dataset.pk, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.accepting_seed || data.accepting_seed == "True") {
          elem.classList.add("ok");
          elem.innerHTML = "&#x2713;";
        } else {
          elem.classList.remove("ok");
          elem.innerHTML = "✖️";
        }
      });
  }
}

function set_plant_accepted(elem) {
  if (elem) {
    fetch("/toggle-plant-accepted/" + elem.dataset.pk, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.is_accepted || data.is_accepted == "True") {
          elem.classList.add("ok");
          elem.innerHTML = "&#x2713;";
        } else {
          elem.classList.remove("ok");
          elem.innerHTML = "✖️";
        }
      });
  }
}
