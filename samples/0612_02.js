onst timer = () => {
        let count = 100;
        const id = setInterval(() => {
                count --;
                console.log(count);
                if (count <= 0) {
                        console.log('end');
                }
        }, 1000);

        return id;
};

const timer_instance = timer();
clearInterval(timer_instance);
