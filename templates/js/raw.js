const g = {
    log: [],
    // input
    inputPath: '',
    outputPath: '',

}

var log = function(...arguments){
    var ter = document.querySelector("#gua-div-terminal")
    let time = new Date()
    arguments.unshift(time.toJSON()+':')
    let line = arguments.join(' ')
    g.log.push(line)
    let s = g.log.join('<br>') 
    s = s + '<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'
    ter.innerHTML = s
}

function getFileData() {
    pywebview.api.getFileData().then(function (response) {
        
    })
}

function getFilePath(){
    // 选择数据目录
    pywebview.api.getFilePath().then((response,  count)=>{
        alertify.alert("输入目录已选择")
        log('response', `(${response})`)
        g.inputPath = response
        // 替换现有的当前任务输入目录
        let s = document.querySelector('#gua-id-span-input-path')
        s.innerHTML = response
        if (count == 0) {
            alertify.error("目录找不到对应文件")
        } else{
            getCountBar("#progressbar")
        }
    })
    // 数据加载进度条
}

function getOutputPath(){
    pywebview.api.getOutputPath().then((response)=>{
        alertify.alert("输出目录已选择")
        g.outputPath = response
        // 替换现有的当前任务输入目录
        let s = document.querySelector('#gua-id-span-output-path')
        s.innerHTML = response
    })
}

function bindEvent(selector, callback) {
    //给一个按钮绑定事件
    let b = document.querySelector(selector)
    b.addEventListener('click', callback)
}

function bar(parent){
    // progressbar.js@1.0.0 version is used
    // Docs: http://progressbarjs.readthedocs.org/en/1.0.0/
    let parentID = parent.slice(1, parent.length)
    let containerID = `${parentID}-container`
    let parentDoc = document.querySelector(parent)
    log(parent)
    log(containerID)
    let html = `
    <div id="${containerID}" class="container"></div>
    `
    parentDoc.insertAdjacentHTML('beforeend', html)
    let container = document.querySelector(`${parent}-container`)
    log(container)
    let bar = new ProgressBar.Circle(container, {
        color: '#333',
        // This has to be the same size as the maximum width to
        // prevent clipping
        strokeWidth: 4,
        trailWidth: 1,
        easing: 'easeInOut',
        duration: 100,
        text: {
            autoStyleContainer: false
        },
        from: { color: '#333', width: 4 },
        to: { color: '#333', width: 4 },
        // Set default step function for all animate calls
        step: function (state, circle) {
            circle.path.setAttribute('stroke', state.color);
            circle.path.setAttribute('stroke-width', state.width);
            var value = Math.round(circle.value() * 100);
            if (value === 0) {
                circle.setText('');
            } else {
                circle.setText(value + '%');
            }
        }
    });
    bar.text.style.fontSize = '2rem';
    return bar
}


function pBar() {
    let parentID = '#progressbar'
    let b = bar(parentID)
    let duration = 100
    let intervalID = setInterval(function(){
        pywebview.api.getCount().then(function(response){
            if (response == "hasEnd") {
                clearInterval(intervalID)
                setTimeout(() => {
                    b.destroy()
                    // 显示表格
                }, 1000);
            } else{
              b.animate(response, {duration: duration})
            }
        })
    }, duration)
}

function getCountBar(parentSelector) {
    // 显示数据的bar
    let parentID = parentSelector
    let b = bar(parentID)
    let duration = 100
    let intervalID = setInterval(function () {
        pywebview.api.getCount().then(function (response) {
            if (response == "noTask") {
                return
            } else if (response == 1.0) {
                clearInterval(intervalID)
                b.animate(response, { duration: duration })
                setTimeout(() => {
                    b.destroy()
                    // 显示表格
                }, 1000);
            } else {
                b.animate(response, { duration: duration })
            }
        })
    }, duration)
}


function main() {
    log("start main function")
    // 给input按钮绑定事件，打开文件
    bindEvent("#gua-a-selector-directory-input", function(){
        getFilePath()
    })
    bindEvent("#gua-a-selector-directory-output", function () {
        getOutputPath()
    })
}

main()