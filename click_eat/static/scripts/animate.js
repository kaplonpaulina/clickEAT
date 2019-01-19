let roller = document.getElementsByClassName("roller")[0];
let i = 1;

setInterval(function () {
    console.log(i);
    switch (i) {
        case 1: {
            roller.classList.add("roll1");
            roller.classList.remove("roll2");

        }; break;
        case 2: {
            roller.classList.remove("roll1");
            roller.classList.add("roll2");
        }; break;
        case 3: {
            roller.classList.remove("roll1");
            roller.classList.remove("roll2");
        }; break;
    }
    i++;
    if (i == 4) i = 1;
}, 2000);