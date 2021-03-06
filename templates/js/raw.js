const g = {
    // 存储日志
    log: [],
    // 存储输入目录input
    inputPath: '',
    // 存储输出目录
    outputPath: '',
    // 是否获取文件
    getFile: false,
    // 文件数据
    fileData: [],
    // 标记任务是否开始
    taskStart: false,
    // 标记标签是否添加
    taskLableAdd: false,
    // sampleData 存放返回的数据, 
    sampleData: [],
    // 标记所有任务是否结束
    taskDone: false,
}

let log = function(...arguments){
    /*
    打印函数
    */
    // let ter = document.querySelector("#gua-div-terminal")
    // let time = new Date()
    // arguments.unshift(time.toJSON()+':')
    // let line = arguments.join(' ')
    // g.log.push(line)
    // let s = g.log.join('<br>') 
    // s = s + '<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'
    // ter.innerHTML = s
}

function mergeTable($table, size, field, rowSpan) {
    /*
    把bootstrap对象根据size和列进行合并
    合并的行数有rowSpan决定
    */
    for (let i = 0; i < size; i += rowSpan) {
        $table.bootstrapTable("mergeCells", { index: i, field: field, rowspan: rowSpan })
    }
    log("run merge")
}


function drawTable(container, data){
    /*
    传入容器来绘制表格
    */
    log("start call draw table func", container)
    let pageSize = 4
    // <th data-field="hash">File Hash</th>
    $(container).prepend(`
    <table id="table" 
    data-page-size="${pageSize}"
    data-page-list="[]"
    data-pagination="true"
    >
    <thead>
            <tr>
                <th data-field="sample">Sample</th>
                <th data-field="name">File Name</th>
                <th data-field="status">Sample Task Status</th>
            </tr>
        </thead>
    </table>
    `) 
    log("table draw table func")
    let $table = $('#table')
    log("draw draw table func")
    $table.bootstrapTable({ 
        data: data,

        onPageChange: function (number, size) {
            mergeTable($table, pageSize, "sample", 2)
            mergeTable($table, pageSize, "status", 2)
        }
    })
    mergeTable($table, pageSize, "sample", 2)
    mergeTable($table, pageSize, "status", 2)
    log("end draw table func")
}

function updateTable($table, field, items){
    for (let index = 0; index < items.length; index++) {
        const value = items[index];
        $table.bootstrapTable('updateCell', {index: index, field: field, value: value})
    }
    let pageSize = 4
    for (let index = 0; index < pageSize; index+=2) {
        log("merge index", index)
        $table.bootstrapTable("mergeCells", {index: index, field: "sample", rowspan: 2})
        $table.bootstrapTable("mergeCells", {index: index, field: field, rowspan: 2})

    }
}

function getFileData(callback) {
    pywebview.api.getFileData().then(function (response) {
        log("response", response)
        for (let index = 0; index < response.length; index++) {
            const element = response[index];
            log("response type", index, JSON.stringify(element))
            g.sampleData.push(element)
        }
        log("globe ", JSON.stringify(g.sampleData))

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
                        if (g.taskLableAdd === false) {
                            $(container).append(`
                            <p>
                            <a id="gua-button-start" href="#" class="pure-button pure-button-primary">Start Task</a>
                            </p>
                            `)
                            g.taskLableAdd = true
                        }
                        alertify.success("配置加载完毕, 请开始任务", 2)
                        g.taskDone = false
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
                log(JSON.stringify(g))
                if (g.inputPath !== '' && g.outputPath !== '') {
                    let container = "#gua-div-table-container"
                    if (g.taskLableAdd === false) {
                        $(container).append(`
                            <p>
                            <a id="gua-button-start" href="#" class="pure-button pure-button-primary">Start Task</a>
                            </p>
                            `)
                        g.taskLableAdd = true
                    }
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
    if (g.taskDone === false) {
        pywebview.api.pipeStart().then(function(response) {
            log("pipeStart response", response)
            // 删除 start 按钮
            $("#gua-button-start").parent().remove()
            g.taskLableAdd = false
        })
    } else {
        alertify.alert("所有任务都已经执行完成")
    }
}

function pipeStatus(taskStatusId) {
    pywebview.api.pipeStatus().then(function(response) {
        if (response.total === response.done) {
            clearInterval(taskStatusId)
            g.taskDone = true
            alertify.alert("所有任务已经执行完毕", function() {})
        } 

        let status = response.status
        let newStatus = []
        let date = new Date().toLocaleString()
        for (let index = 0; index < status.length; index++) {
            const element = status[index];
            if (element.startsWith("done") || element === "waiting"){
                newStatus.push(element)
                newStatus.push(element)
            } else{
                newStatus.push(element + "<br>" + date)
                newStatus.push(element + "<br>" + date)
            }
        }
        // remove table
        let pageSize = 4
        log("status", JSON.stringify(status))
        log("new status", JSON.stringify(newStatus))
        updateTable( $("#table"), "status", newStatus)
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
    bindEvent("body", function (event) {
        let self = event.target
        log("click start", self.id)
        if (self.id === "gua-button-start") {
            pipeStart()
            // 切换场景为table进度条
            let taskStatusId = setInterval(function(){
                pipeStatus(taskStatusId)
            }, 1000)
        }
    })
    log("end main function")
}

main()