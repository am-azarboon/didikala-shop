const ResendBtn = document.getElementById("resendBtn");
const ResendTimer = document.getElementById("resendTimer");

let time = [1, 59, 0];
let valid_send = false;
let interval = setInterval(timer, 10);


function send(e){
    e.preventDefault();

    if(valid_send) {
        $.get("otp-send").then(response =>{
            if(response["status"] === "sent"){
                valid_send = false;
                time[0] = 1;

                ResendBtn.innerHTML = "";
                interval = setInterval(timer, 10)
            }
            else {
                window.location = "/";
            }
        })
    }
}

function timer(){
    ResendTimer.innerHTML = "(" + time[0] + ":" + time[1] + ")";
    time[2]++;

    if(time[2] >= 100){
        time[2] = 0;
        --time[1];

        if(time[1] < 0) {
            --time[0];

            if(time[0] <= 0){
                clearInterval(interval);
                time[2] = 0;
                valid_send = true;

                ResendBtn.innerHTML = "ارسال مجدد کد";
            }
            time[1] = 59;
        }
    }
}

ResendBtn.addEventListener("click", send);
