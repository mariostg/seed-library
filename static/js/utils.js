let acc = document.querySelectorAll(".sheet__detail h3");
for (let c of acc) {
  c.addEventListener("click", function () {
    let children = this.parentNode.children;
    for (let c of children) {
      if (c.tagName != "H3") {
        if (c.classList.contains("show")) {
          c.classList.replace("show", "hide");
        } else {
          c.classList.replace("hide", "show");
        }
        // c.classList.toggle("toggable");
      }
    }
  });
}
