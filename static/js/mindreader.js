function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

function start_progress(){
    var my_progree_bar = document.getElementById("my-progress-bar");
    var my_progree_bar_child = document.getElementById("my-progress-bar-child");
    var usernumber = document.getElementById("user-number");


    for(var i=0; i<100; i++){
        my_progree_bar.setAttribute("aria-valuenow", i);
        my_progree_bar_child.setAttribute("style", "width: "+ i + "%");
        console.log(i);
        sleep(50000);
    }
    usernumber.classList.toggle('hide-text');
}