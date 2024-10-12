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

var currentSongData = {
	title: "None",
	artist: "None",
	audio_id: 0,
	thumbnail_id: 0
}

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
			title: currentSongData.title,
			artist: currentSongData.artist,
			artwork: [
				{ src: `/files/images/${currentSongData.thumbnail_id}`, sizes: "512x512" }
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

function updateAudioPlayer() {
	miniPlayerAudioNode.src = `/files/audio/${currentSongData.audio_id}`;
	miniPlayerCover.src = `/files/images/${currentSongData.thumbnail_id}`;
	updateMedioSess();
	updateTimes();
}

function setMiniPlayerSong(song_id) {
	fetch(`/songs/${song_id}`)
		.then((r) => {
			return r.json();
		})
		.then((data) => {
			currentSongData = data;
			updateAudioPlayer();
			pauseAudio();
		});
};

setMiniPlayerSong(1);
