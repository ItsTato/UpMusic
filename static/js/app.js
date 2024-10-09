console.log("\
 _____       _____            _      \n\
|  |  | ___ |     | _ _  ___ |_| ___ \n\
|  |  || . || | | || | ||_ -|| ||  _|\n\
|_____||  _||_|_|_||___||___||_||___|\n\
       |_|                           \n\
");

const homeButton = document.getElementById("home-button");
const libraryButton = document.getElementById("library-button");

const miniPlayerAudioNode = document.getElementById("mini-player-audio");
const miniPlayerPlayButton = document.getElementById("mini-player-play");
const miniPlayerBarFilled = document.getElementById("mini-player-bar-filled");
const miniPlayerCover = document.getElementById("mini-player-cover");

const miniPlayerCurrentTime = document.getElementById("mini-player-current");
const miniPlayerDurationTime = document.getElementById("mini-player-duration");

miniPlayerAudioNode.controls = false;

function updateTimes() {
	miniPlayerCurrentTime.textContent = new Date(miniPlayerAudioNode.currentTime*1000)
		.toISOString()
		.substr(11,8);
	miniPlayerDurationTime.textContent = new Date(miniPlayerAudioNode.duration*1000)
		.toISOString()
		.substr(11,8);
};

function playAudio() {
	miniPlayerAudioNode.play();
	miniPlayerPlayButton.src = "/static/icons/pause.png";
};

function pauseAudio() {
	miniPlayerAudioNode.pause();
	miniPlayerPlayButton.src = "/static/icons/play.png";
}

function updateMedioSess() {
	if ("mediaSession" in navigator) {
		navigator.mediaSession.metadata = new MediaMetadata({
			title: "Mr. Blue Sky",
			artist: "Electric Light Orchestra",
			artwork: [
				{ src: miniPlayerCover.src, sizes: "512x512" }
			]
		});

		navigator.mediaSession.setActionHandler("play", () => {
			playAudio();
		});

		navigator.mediaSession.setActionHandler("pause", () => {
			pauseAudio();
		});
	};
};

miniPlayerPlayButton.addEventListener("click", (e) => {
	updateMedioSess();
	if (miniPlayerAudioNode.paused) {
		playAudio();
	} else {
		pauseAudio();
	}
});

miniPlayerAudioNode.addEventListener("timeupdate", (e) => {
	updateTimes();
	const prog = (100/(miniPlayerAudioNode.duration*1000))*(miniPlayerAudioNode.currentTime*1000);
	miniPlayerBarFilled.style.width = `${prog}%`;
	if (prog == 100) {
		miniPlayerPlayButton.src = "/static/icons/play.png";
	};
});
