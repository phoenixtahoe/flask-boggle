class Boggle {
    constructor(board, seconds) {
        this.board = $("#" + board);
        this.seconds = seconds
        this.score = 0
        this.words = new Set();
        this.timer = setInterval(this.tick.bind(this), 1000);
        
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }
    async tick() {
        this.seconds -= 1;
        this.showTimer()
    
        if (this.seconds === 0) {
          clearInterval(this.timer);
          await this.endGame()
        }
    }
    async handleSubmit(evt) {
        evt.preventDefault();
        const $word = $(".word", this.board);
    
        let word = $word.val();
        if (!word) return;
    
        if (this.words.has(word)) {
          this.showMessage(`Already found ${word}`, "err");
          return;
        }
        const resp = await axios.get("/check", { params: { word: word }});
        if (resp.data.result === "not-word") {
          this.showMessage(`${word} is not a valid word`, "err");
        } 
        else if (resp.data.result === "not-on-board") {
          this.showMessage(`${word} is not on this board`, "err");
        } 
        else {
          this.showWord(word);
          this.score += word.length;
          this.showScore();
          this.words.add(word);
          this.showMessage(`Added: ${word}`, "ok");
        }
    
        $word.val("").focus();
      }
      async endGame() {
        $(".add-word", this.board).hide();
        const resp = await axios.post("/post-score", { score: this.score });
        if (resp.data.brokeRecord) {
          this.showMessage(`New record: ${this.score}`, "ok");
        } else {
          this.showMessage(`Final score: ${this.score}`, "ok");
        }
      }
      showMessage(msg, cls) {
        $(".msg", this.board)
          .text(msg)
          .removeClass()
          .addClass(`msg ${cls}`);
      }
      showWord(word) {
        $(".words", this.board).append($("<li>", { text: word }));
      }
      showScore() {
        $(".score", this.board).text(this.score);
      }
      showTimer() {
        $(".timer", this.board).text(this.seconds);
      }
}