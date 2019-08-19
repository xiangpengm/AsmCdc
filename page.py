html = """
    <!DOCTYPE html>
<html>

<head lang="en">
    <meta charset="UTF-8">
    <style>
        #response-container {
    display: none;
    padding: 3rem;
    margin: 3rem 5rem;
    font-size: 120%;
    border: 5px dashed #ccc;
}

label {
    margin-left: 0.3rem;
    margin-right: 0.3rem;
}

button {
    font-size: 100%;
    padding: 0.5rem;
    margin: 0.3rem;
    text-transform: uppercase;
}
    </style>
</head>

<body>
    <h1>JS API Example</h1>
    
    <!-- btn1 -->
    <div>
    <button onClick="initialize()">Hello Python</button><br />
    </div>
    
    <!-- btn2 -->
    <div>
    <button id="heavy-stuff-btn" onClick="doHeavyStuff()">Perform a heavy operation</button><br />
    </div>

    <!-- btn3 -->
    <div>
    <button onClick="getRandomNumber()">Get a random number</button>
    </div>
    
    <!-- btn4 -->
    <div>
    <label for="name_input">Say hello to:</label>
    <input id="name_input" placeholder="put a name here">
    <button onClick="greet()">Greet</button><br />
    </div>

    <div>
        <button onclick="getFile()">选择文件</button>
    </div>
    
    <div>
        <button onclick="saveFile()">选择文件</button>
    </div>
    <!-- 容器 -->
    <div id="response-container">
    </div>
    <script>
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
    </script>
</body>

</html>
"""