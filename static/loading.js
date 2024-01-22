document.addEventListener("DOMContentLoaded", function () {
  var runTestButtons = document.querySelectorAll(".run-test-button");

  runTestButtons.forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault();
      var form = button.closest("form");
      button.style.display = "none";
      var loadingModule = form.querySelector(".loading-module");
      loadingModule.style.display = "block";

      // After a delay, submit the form
      setTimeout(function () {
        form.submit();
      }, 3000); // Simulated delay of 3 seconds
    });
  });
});
