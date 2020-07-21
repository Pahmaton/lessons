URL = "/voice/recognize/"

navigator.mediaDevices.getUserMedia({ audio: true})
    .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        let voice = [];
        document.querySelector('#start').addEventListener('click', function(){
            mediaRecorder.start();
        });

        mediaRecorder.addEventListener("dataavailable",function(event) {
            voice.push(event.data);
        });

        document.querySelector('#stop').addEventListener('click', function(){
            mediaRecorder.stop();
        });

        mediaRecorder.addEventListener("stop", function() {
            const audioBlob = new Blob(voice, {
                type: 'audio/wav'
            });

            let fd = new FormData();
            fd.append('voice', audioBlob);
            sendVoice(fd);
            voice = [];
        });
    });

async function sendVoice(form) {
    let promise = await fetch(URL, {
        method: 'POST',
        body: form});
    if (promise.ok) {
        let response = await promise.json();
        console.log(response);
        let audio = document.createElement('p');
        audio.textContent = response.text;
        document.querySelector('#messages').appendChild(audio);
    }
}
