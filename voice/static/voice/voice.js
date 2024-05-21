recognizeUrl = "/voice/recognize/"

const record = document.getElementById('start');
const stop = document.getElementById('stop');
const container = document.getElementById('messages');
let audio_context;
let recorder;

function startUserMedia(stream) {
    audio_context = new AudioContext;
    let input = audio_context.createMediaStreamSource(stream);
    recorder = new Recorder(input, {numChannels: 1});
}

function startRecording(button) {
    recorder && recorder.record();
    button.disabled = true;
    var stop = document.getElementById('stop');
    stop.disabled = false;
    button.nextElementSibling.disabled = false;
}

function stopRecording(button) {
    recorder && recorder.stop();
    button.disabled = true;
    button.previousElementSibling.disabled = false;
    var last_el = document.getElementById('last_el');
    // create WAV download link using audio data blob
    createDownloadLink();
    $("<div class='container'><div class='row justify-content-center'><div class='spinner-border text-dark' role='status'><span class='sr-only'>Loading...</span></div></div><div class='row justify-content-center'>Подождите, текст распознается...</div></div>").insertAfter(last_el);
    recorder.clear();
    button.disabled = false;
  }

function createDownloadLink() {
    recorder && recorder.exportWAV(function(blob) {
      const formData = new FormData();
      formData.append('voice', blob);
      fetch(recognizeUrl, {
          method: 'POST',
          body: formData
        })
        .then((response) => response.json())
        .then((result) => {
          console.log('Success:', result);
          $('<div>123</div>')
          window.location.href = 'my_files/';
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    });
  }

window.onload = function init() {
    navigator.mediaDevices.getUserMedia({audio: true}).then((stream) => startUserMedia(stream));
};
