const g = {
    log: [],
    // input
    inputPath: '',
    outputPath: '',
    getFile: false,
    fileData: [],
    taskStart: false,
}

let log = function(...arguments){
    let ter = document.querySelector("#gua-div-terminal")
    let time = new Date()
    arguments.unshift(time.toJSON()+':')
    let line = arguments.join(' ')
    g.log.push(line)
    let s = g.log.join('<br>') 
    s = s + '<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'
    ter.innerHTML = s
}

function drawTable(container, data){
    log("start call draw table func", container)
        $(container).prepend(`
        <table id="table" 
        data-page-size="2"   
        data-pagination="true"
        >
            <thead>
                <tr>
                    <th data-field="id">ID</th>
                    <th data-field="sample">Sample</th>
                    <th data-field="name">File Name</th>
                    <th data-field="hash">File Hash</th>
                    <th data-field="status">Item Status</th>
                </tr>
            </thead>
        </table>
    `) 
    log("table draw table func")
    let $table = $('#table')
    log("draw draw table func")
    $table.bootstrapTable({ data: data })
    log("end draw table func")
}


function getFileData(callback) {
    pywebview.api.getFileData().then(function (response) {
        drawTable("#gua-div-table-container", response)
        callback()
    })
}

function getFilePath(){
    // 选择数据目录
    pywebview.api.getFilePath().then((params)=>{
        log('response', `(${params.path})`, params.total)
        if (params === "None") {
            alertify.error("未选择目录, 请重新选择目录", 2)
        }else if (params.total === 0) {
            alertify.error("目录找不到对应文件, 请重新选择目录", 2)
        } else{
            g.getFile = true
            g.inputPath = params.path
            // 替换现有的当前任务输入目录
            let s = document.querySelector('#gua-id-span-input-path')
            s.innerHTML = params.path
            alertify.alert("CDC ASM Client", "输入目录已选择")
            getCountBar("#progressbar", function () {
                // 获取数据
                getFileData(function(){
                    if (g.inputPath !== '' && g.outputPath !== '') {
                        let container = "#gua-div-table-container"
                        $(container).append(`
                                <p>
                                    <a id="gua-button-start" href="#" class="pure-button pure-button-primary">Start Task</a>
                                </p>
                        `)
                        alertify.success("配置加载完毕, 请开始任务", 2)
                    }
                })
            })
        }
    })
    // 数据加载进度条
}

function getOutputPath(){
    pywebview.api.getOutputPath().then((response)=>{
        if (response === 'None') {
            alertify.error("未选择输出目录, 请重新选择目录", 2)
        } else if(g.getFile === true){
            alertify.error("等待输入目录数据加载完成", 2)
        } else {
            g.outputPath = response
            // 替换现有的当前任务输入目录
            let s = document.querySelector('#gua-id-span-output-path')
            s.innerHTML = response
            alertify.alert("输出目录已选择", function(){
                if (g.inputPath !== '' && g.outputPath !== '') {
                    let container = "#gua-div-table-container"
                    $(container).append(`
                            <p>
                                <a id="gua-button-start" href="#" class="pure-button pure-button-primary">Start Task</a>
                            </p>
                    `)
                    alertify.success("配置加载完毕, 请开始任务", 2)
                }
            })
        }
    })
}

function bindEvent(selector, callback) {
    //给一个按钮绑定事件
    log("bind Event", selector)
    let b = document.querySelector(selector)
    b.addEventListener('click', callback)
}

function bar(parent){
    // progressbar.js@1.0.0 version is used
    // Docs: http://progressbarjs.readthedocs.org/en/1.0.0/
    // 删除原来表格
    if ($("#table").length > 0){
        let $table = $("#table")
        $table.bootstrapTable("removeAll")
        $table.bootstrapTable("destroy")
        $table.remove()
    }
    if ($("#gua-button-start").length > 0) {
        $("#gua-button-start").remove()
    }
    let parentID = parent.slice(1, parent.length)
    let containerID = `${parentID}-container`
    let parentDoc = document.querySelector(parent)
    let html = `
    <div id="${containerID}" class="container"></div>
    `
    parentDoc.insertAdjacentHTML('beforeend', html)
    let container = document.querySelector(`${parent}-container`)
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
                circle.setText('loading');
            } else {
                circle.setText(value + '%');
            }
        }
    });
    bar.text.style.fontSize = '2rem';
    return bar
}

function getCountBar(parentSelector, callback) {
    // 显示数据的bar
    let parentID = parentSelector
    let b = bar(parentID)
    let duration = 100
    let intervalID = setInterval(function () {
        pywebview.api.getCount().then(function (response) {
            if (response === "noTask") {
                
            } else if (response === 1.0) {
                clearInterval(intervalID)
                b.animate(response, { duration: duration })
                setTimeout(() => {
                    b.destroy()
                    g.getFile = false
                    let s = document.querySelector(parentID)
                    s.innerHTML = ''
                    callback()
                    // 显示表格
                }, 1000);
            } else {
                b.animate(response, { duration: duration })
            }
        })
    }, duration)
}

function pipeStart() {
    pywebview.api.pipeStart().then(function(response) {
        log("pipeStart response", response)
    })
}

function pipeStatus() {
    pywebview.api.pipeStatus().then(function(response) {
        log("pipeStatus response", response)
    })
}


function main() {
    log("start main function")
    alertify.defaults.glossary.title = "CDC ASM Client"
    // // 给input按钮绑定事件，打开文件
    bindEvent("#gua-a-selector-directory-input", function(){
        getFilePath()
    })
    bindEvent("#gua-a-selector-directory-output", function () {
        getOutputPath()
    })
    bindEvent("#gua-a-selector-start", function () {
        pipeStart()
    })
    bindEvent("#gua-a-selector-status", function () {
        pipeStatus()
    })
    log("end main function")
}

main()