function listen() {
    var source = new EventSource("/stream/");
    var target = document.getElementById("placeholder");
    source.onmessage = function(msg) {
	target.innerHTML = msg.data + '<br>';
    }
}

listen();
