$(document).ready(function () {
  $("#guessForm").on("submit", function (e) {
    e.preventDefault(); //Stop the form from submitting

    var word = $('input[name="word"]').val(); //Use jQuery to get value of input

    axios
      .post("/check-word", { word: word })
      .then(function (response) {
        if (response.data.result === "ok") {
          alert("Correct!");
          updateScore(response.data.score);
        } else if (response.data.result === "not-on-board") {
          alert("Word is not on the board!");
        } else {
          alert("Not a valid word!");
        }
      })

      .catch(function (error) {
        alert("Error processing your guess.");
      });
    function updateScore(newScore) {
      $("#score").text(newScore);
    }
  });
});
