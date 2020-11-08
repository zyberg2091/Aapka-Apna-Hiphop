w = screen.width
if(w < 768){
    document.querySelector(".video-con").style.display = "block"
}
document.querySelector("#submit-button").addEventListener('click', function () {
    const text = document.getElementById("text-input").value;
    document.getElementById("output-text").innerHTML = "<center><svg class=\"filter\" version=\"1.1\"><defs><filter id=\"gooeyness\"><feGaussianBlur in=\"SourceGraphic\" stdDeviation=\"10\" result=\"blur\" /><feColorMatrix in=\"blur\" mode=\"matrix\" values=\"1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 20 -10\" result=\"gooeyness\" /><feComposite in=\"SourceGraphic\" in2=\"gooeyness\" operator=\"atop\" /></filter></defs></svg><div class=\"dots\"><div class=\"dot mainDot\"></div><div class=\"dot\"></div><div class=\"dot\"></div><div class=\"dot\"></div><div class=\"dot\"></div></div></center>"
    let message = {
        initialWords: text,
        artist: document.getElementsByTagName("body")[0].id
    }
    $.post("https://aapka-apna-hip-hop.herokuapp.com/predict", JSON.stringify(message), function (response){
        speakLyrics(response)
        var res = response.split(" ")
        document.getElementById("output-text").innerHTML = "<strong>The generated bars are :</strong> <br>"
        var Timer = setInterval(printEle, 200);
        var index = 0;
        function printEle(){
            if(index == res.length){
                clearInterval(Timer)
            }else{
                document.getElementById("output-text").innerHTML = document.getElementById("output-text").innerText + " " + res[index];
                index++;
            }
        }
    })
})
var voiceList = document.querySelector('#voiceList');
var synth = window.speechSynthesis;
var voices = [];
PopulateVoices();
if(speechSynthesis !== undefined){
    speechSynthesis.onvoiceschanged = PopulateVoices;
}
function speakLyrics(txtOutput){
    var toSpeak = new SpeechSynthesisUtterance(txtOutput);
    var selectedVoiceName = voiceList.selectedOptions[0].getAttribute('data-name');
    voices.forEach((voice)=>{
        if(voice.name === selectedVoiceName){
            toSpeak.voice = voice;
        }
    });
    synth.speak(toSpeak);
}
function PopulateVoices(){
    voices = synth.getVoices();
    var selectedIndex = voiceList.selectedIndex < 0 ? 0 : voiceList.selectedIndex;
    voiceList.innerHTML = '';
    voices.forEach((voice)=>{
        var listItem = document.createElement('option');
        listItem.textContent = voice.name;
        listItem.setAttribute('data-lang', voice.lang);
        listItem.setAttribute('data-name', voice.name);
        voiceList.appendChild(listItem);
    });
    voiceList.selectedIndex = selectedIndex;
}