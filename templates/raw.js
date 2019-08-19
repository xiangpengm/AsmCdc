function showResponse(response) {
    var container = document.getElementById('response-container')

    container.innerText = response.message
    container.style.display = 'block'
}

function initialize() {
    pywebview.api.init().then(showResponse)
}

function doHeavyStuff() {
    var btn = document.getElementById('heavy-stuff-btn')

    pywebview.api.doHeavyStuff().then(function (response) {
        showResponse(response)
        btn.onclick = doHeavyStuff
        btn.innerText = 'Perform a heavy operation'
    })

    showResponse({ message: 'Working...' })
    btn.innerText = 'Cancel the heavy operation'
    btn.onclick = cancelHeavyStuff
}

function cancelHeavyStuff() {
    pywebview.api.cancelHeavyStuff()
}

function getRandomNumber() {
    pywebview.api.getRandomNumber().then(showResponse)
}

function greet() {
    var name_input = document.getElementById('name_input').value;
    pywebview.api.sayHelloTo(name_input).then(showResponse)
}

function getFile(){
    pywebview.api.getFile().then(showResponse)
    // showResponse({ message: "file"})
}

function saveFile() {
    pywebview.api.saveFile().then(showResponse)
    // showResponse({ message: "file"})
}



function main() {

}


main()