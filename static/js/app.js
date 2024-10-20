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
const miniPlayerName = document.getElementById("mini-player-name");
const miniPlayerArtist = document.getElementById("mini-player-artist");
const miniPlayerLoopButton = document.getElementById("mini-player-loop");
const miniPlayerLoopButtonIcon = document.getElementById("mini-player-loop-icon");
const miniPlayerLikeButton = document.getElementById("mini-player-like");
const miniPlayerLikeButtonIcon = document.getElementById("mini-player-like-icon");
const miniPlayerCurrentTime = document.getElementById("mini-player-current");
const miniPlayerDurationTime = document.getElementById("mini-player-duration");

var currentSongData = {
	song_id: 0,
	title: "None",
	artist: "None",
	thumbnail_id: 0,
	audio_id: 0
}

miniPlayerAudioNode.controls = false;

function updateTimes() {
	miniPlayerCurrentTime.textContent = new Date(miniPlayerAudioNode.currentTime*1000)
	.toISOString()
	.substr(11,8)
	.substr(3,7);
	miniPlayerDurationTime.textContent = new Date(miniPlayerAudioNode.duration*1000)
	.toISOString()
	.substr(11,8)
	.substr(3,7);
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

miniPlayerLoopButton.addEventListener("click", (e) => {
	if (!miniPlayerAudioNode.loop) {
		miniPlayerLoopButton.className = "mini-player-loop-active";
		miniPlayerAudioNode.loop = true;
	} else {
		miniPlayerLoopButton.className = "mini-player-loop";
		miniPlayerAudioNode.loop = false;
	};
});

function isLiked(song_id) {
	return fetch(`/api/songs/${song_id}/like`, {
		method: "GET",
		headers: {
			"Content-Type": "application/json"
		}
	})
	.then(res => res.json())
	.then(data => {
		return data["Liked"];
	});
};

function likeSong(song_id) {
	return fetch(`/api/songs/${song_id}/like`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		}
	})
	.then(res => res.json())
	.then(data => {
		return data["Liked"];
	});
};

function unlikeSong(song_id) {
	return fetch(`/api/songs/${song_id}/like`, {
		method: "DELETE",
		headers: {
			"Content-Type": "application/json"
		}
	})
	.then(res => {return res.json()})
	.then(data => {
		return data["Liked"];
	});
};

miniPlayerLikeButton.addEventListener("click", (e) => {
	isLiked(currentSongData["song_id"]).then(isLiked => {
		if (isLiked) {
			unlikeSong(currentSongData["song_id"]);
			miniPlayerLikeButton.className = "mini-player-like";
			miniPlayerLikeButtonIcon.src = "/static/icons/like.png";
		} else {
			likeSong(currentSongData["song_id"]);
			miniPlayerLikeButton.className = "mini-player-like-active";
			miniPlayerLikeButtonIcon.src = "/static/icons/remove.png";
		};
	});
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
	miniPlayerAudioNode.src = `/files/audios/${currentSongData.audio_id}`;
	miniPlayerCover.src = `/files/images/${currentSongData.thumbnail_id}`;
	miniPlayerName.innerText = currentSongData.title;
	miniPlayerArtist.innerText = currentSongData.artist;
	updateMedioSess();
	updateTimes();
};

function setMiniPlayerSong(song_id) {
	fetch(`/api/songs/${song_id}`)
	.then((r) => {
		return r.json();
	})
	.then((data) => {
		currentSongData = data;
		currentSongData["song_id"] = song_id;
		isLiked(song_id).then(isLiked => {
			if (isLiked) {
				miniPlayerLikeButton.className = "mini-player-like-active";
				miniPlayerLikeButtonIcon.src = "/static/icons/remove.png";
			} else {
				miniPlayerLikeButton.className = "mini-player-like";
				miniPlayerLikeButtonIcon.src = "/static/icons/like.png";
			};
		});
		pauseAudio();
		updateAudioPlayer();
	});
};

setMiniPlayerSong(1);
