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
    button.nextElementSibling.disabled = false;
}

function stopRecording(button) {
    recorder && recorder.stop();
    button.disabled = true;
    button.previousElementSibling.disabled = false;

    // create WAV download link using audio data blob
    createDownloadLink();
    $('<div class="alert alert-info alert-dismissible fade show notification" role="alert"><strong>Поздравляю!</strong> Запись успешно завершена. <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>').insertAfter("form");
    recorder.clear();
    button.disabled = false;

  }

function createDownloadLink() {
    recorder && recorder.exportWAV(function(blob) {
      var url = URL.createObjectURL(blob);
      var li = document.createElement('li');
      var au = document.createElement('audio');
      var hf = document.createElement('a');

      au.controls = true;
      au.src = url;
      hf.href = url;
      hf.download = new Date().toISOString() + '.wav';
      hf.innerHTML = hf.download;
      li.appendChild(au);
      li.appendChild(hf);
      container.appendChild(li);


      const formData = new FormData();
      formData.append('voice', blob);
      fetch(recognizeUrl, {
          method: 'POST',
          body: formData
        })
        .then((response) => response.json())
        .then((result) => {
          console.log('Success:', result);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    });
  }

window.onload = function init() {
    navigator.mediaDevices.getUserMedia({audio: true}).then((stream) => startUserMedia(stream));
};
