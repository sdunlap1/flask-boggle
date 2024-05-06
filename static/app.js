$(document).ready(function () {
  class BoggleGame {
    constructor(seconds = 10) {
      this.seconds = seconds;
      this.score = 0;
      this.timer = null;
      this.updateTimerDisplay();
    }

    startTimer() {
      this.timer = setInterval(() => {
        if (this.seconds > 0) {
          this.seconds--;
          this.updateTimerDisplay();
        } else {
          this.endGame();
        }
      }, 1000);
    }

    updateTimerDisplay() {
      $("#countdown").text(this.seconds); // Ensure this matches the ID in your HTML
    }

    updateScore(newScore) {
      this.score += newScore; // Update the internal score
      $("#score").text(this.score); // Update the score display
    }

    endGame() {
      clearInterval(this.timer); // Stop the timer
      this.timer = null;
      $("#guessForm button").prop("disabled", true); // Disable submit button after timer reaches 0
      axios
        .post("/post-score", { score: this.score })
        .then((response) => {
          alert("Game Over! Final Score Posted: " + this.score); // took forever to figure this one out!
          this.score = 0;
          $("#score").text(this.score);
        })
        .catch((error) => {
          console.error("Error posting score:", error);
          alert("Error posting score.");
        });
    }
  }

  const game = new BoggleGame();
  game.startTimer();

  $("#guessForm").on("submit", function (e) {
    e.preventDefault(); // Stop the form from submitting

    var word = $('input[name="word"]').val(); // Use jQuery to get value of input

    axios
      .post("/check-word", { word: word })
      .then(function (response) {
        if (response.data.result === "ok") {
          alert("Correct!");
          game.updateScore(word.length);
        } else if (response.data.result === "already-submitted") {
          alert("YOU ALREADY SUBMITTED THIS WORD! CHEATER!!");
        } else if (response.data.result === "not-on-board") {
          alert("Word is not on the board!");
        } else {
          alert("Not a valid word!");
        }
      })
      .catch(function (error) {
        alert("Error processing your guess.");
        console.error("Submission error: ", error);
      });

    function updateScore(newScore) {
      $("#score").text(newScore);
    }
  });
  // Add a button for starting new game
  $("#restart-game").on("click", function () {
    window.location.reload();
  });
});
