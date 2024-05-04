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
      });
    function updateScore(newScore) {
      $("#score").text(newScore);
    }
  });
});

class BoggleGame {
  constructor(seconds = 60) {
    this.seconds = seconds;
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
    $("#timer").text(this.seconds);
  }

  endGame() {
    axios
      .post("/post-score", { score: this.score })
      .then((response) => {
        alert("Final Score Posted");
      })
      .catch((error) => {
        console.error("Error posting score:", error);
      });
  }
}

$(document).ready(() => {
  const game = new BoggleGame(60);
  game.startTimer();
});