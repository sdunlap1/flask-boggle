$(document).ready(function () {
  class BoggleGame {
    constructor(seconds = 60, score= 0) {
      this.seconds = seconds;
      this.score = score;
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
      $("#countdown").text(this.seconds);  // Ensure this matches the ID in your HTML
    }

    endGame() {
      clearInterval(this.timer); // Stop the timer
      axios.post("/post-score", { score: this.score })
        .then(response => {
          alert("Game Over! Final Score Posted: " + response.data.high_score);
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

    axios.post("/check-word", { word: word })
      .then(function (response) {
        if (response.data.result === "ok") {
          alert("Correct!");
          updateScore(response.data.score);
        } else if (response.data.result === "already-submitted") {
          alert("You already submitted this word! Cheater!!");
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
});
