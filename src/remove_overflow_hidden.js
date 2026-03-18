// This is just here to remove overflow hidden from websites that block scrolling

setInterval(() => {
  document.body.style.setProperty("overflow", "visible", "important");
  document.documentElement.style.setProperty("overflow", "visible", "important");
}, 100);