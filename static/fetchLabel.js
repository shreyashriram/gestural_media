var player;

var fetch_label = function() { 

    fetch('/fetchLabel').then(response => response.json()).then(function(data){

        var label = data['updated_label']

        document.getElementById("to_change").innerHTML = label;

        if (label == "PAUSE") {
            stop();
        } else if (label == "PLAY") {
            play();
        } else if (label == "PREVIOUS TRACK") {
            lastVideo();
        } else if (label == "NEXT TRACK") {
            nextVideo();
        } else if (label == "FAST FORWARD 10 SEC") {
            next();
        } else if (label == "REWIND 10 SEC") {
            back();
        } else {
            nothing();
        }
    });
};

// call the fetch_label function every 1/2 seconds
var timeOut = setInterval(fetch_label, 500);

function stop() {
    var myEl = document.getElementById("stream")
    myEl.style.boxShadow = "0px 0px 50px red";


    myEl = document.getElementById("icon")
    myEl.src="static/assets/pause.svg";
    myEl.style.visibility="visible";

    player.pauseVideo();
}

function play() {
    var myEl = document.getElementById("stream")
    myEl.style.boxShadow = "0px 0px 50px green";

    myEl = document.getElementById("icon")
    myEl.src="static/assets/play.svg";
    myEl.style.visibility="visible";

    player.playVideo();
}

function next() {
    var myEl = document.getElementById("stream")
    myEl.style.boxShadow = "20px 0px 10px blue";

    myEl = document.getElementById("icon")
    myEl.src="static/assets/fastforward.svg";
    myEl.style.visibility="visible";
    fastForward();
}

function nextVideo() {
    var myEl = document.getElementById("stream")
    myEl.style.boxShadow = "20px 0px 10px rgb(255, 221, 2)";

    myEl = document.getElementById("icon")
    myEl.src="static/assets/next.svg";
    myEl.style.visibility="visible";
    fastForward();
}

function back() {
    var myEl = document.getElementById("stream")
    myEl.style.boxShadow = "-20px 0px 10px blue";

    myEl = document.getElementById("icon")
    myEl.src="static/assets/rewind.svg";
    myEl.style.visibility="visible";

    // player.stopVideo();
    rewind();
}

function lastVideo() {
    var myEl = document.getElementById("stream")
    myEl.style.boxShadow = "-20px 0px 10px rgb(255, 221, 2)";

    myEl = document.getElementById("icon")
    myEl.src="static/assets/previous.svg";
    myEl.style.visibility="visible";

    player.stopVideo();
}

function nothing() {
    var myEl = document.getElementById("stream")
    myEl.style.boxShadow = "0px 0px";

    myEl = document.getElementById("icon")
    myEl.style.visibility="hidden";
}

function onYouTubePlayerAPIReady() {
    // create the global player from the specific iframe (#video)
    player = new YT.Player('video', {
        events: {
            // call this function when player is ready to use
            'onReady': onPlayerReady
        }
    });
}

function onPlayerReady(event) {

    // bind events
    // var playButton = document.getElementById("play-video");

    if(event == "PLAY"){
        playButton.addEventListener(event, function() {
            player.playVideo();
        });
    }
    if(event == "STOP"){
        // var pauseButton = document.getElementById("pause-video");
        pauseButton.addEventListener(event, function() {
            player.pauseVideo();
        });
    }
}

function fastForward(){
    var currentTime = player.getCurrentTime();
    if(currentTime < (currentTime + 10)){
        player.seekTo(currentTime + 10, true);
        player.playVideo();
    } else {
        player.stopVideo();
        console.log("Try to fast forward video when current playing time greater than 10.");
    }
}

function rewind(){
    var currentTime = player.getCurrentTime();
    if(currentTime > (currentTime - 10)){
        player.seekTo(currentTime - 10, true);
        player.playVideo();
    } else {
        player.stopVideo();
        console.log("Try to rewind video when current playing time greater than 10.");
    }
}

// Inject YouTube API script
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);