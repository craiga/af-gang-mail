const flatpickr = require("flatpickr");

document.addEventListener("DOMContentLoaded", function (event) {
  flatpickr(".datetimeinput", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
  });
});
