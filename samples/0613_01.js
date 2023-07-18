
/* エラーが出るコード */
// 変数Timerの引数にcallbackとcountdown
let Timer = (callback, countdown) => {
  // 変数idとtimeは引数countdownへ
  let id, timer = countdown;
  // タイマー部分のHTML要素（p要素）を取得する
  // 2重で変数を定義できない、let id, time = count.textContentが正しい？
  timer = count.textContent;

  // この変数内でpauseという関数を用意、idをタイムアウトさせる
  this.pause = () => {
    clearTimeout(id);
    id = null;
  };

  // この変数内でresumeという関数を用意、idを取得し値を戻させる
  this.resume = () => {
    if (id) {
      return;
    }

    // インターバルのセット
    id = setInterval(() => {
      // １秒ごとにマイナスする
      timer--;
      // タイマー部分のHTML要素（p要素）を取得する
      count.textContent = timer;
      console.log(timer);
      // もしゼロになったら
      if (timer <= 0) {
        // gameOver関数でスコア表示
        //gameOver(id);
        // なぜここでcallbackが来るのか？
        callback();
      }
    }, 1000);
  };
};
