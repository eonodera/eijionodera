let Timer = function(callback, count) {
    let timerId, start, remaining = count;

    this.pause = function() {
        clearTimeout(timerId);
        timerId = null;
    };

    this.resume = function() {
        if (timerId) {
            return;
        }

        timerId = setInterval(() => {
	    remaining --;
            console.log(remaining);
            if (remaining<= 0) {
	        console.log('end');
		callback();
	        clearTimeout(timerId);
            }
        }, 1000);
    };

    this.resume();
};

var timer = new Timer(function() {
    console.log("Done!");
}, 1000);


timer.pause();
timer.resume();
