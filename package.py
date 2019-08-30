import os
import webview
from jinja2 import (
    FileSystemLoader,
    Environment)


def load(file, tp='r'):
    with open(file, tp) as f:
        return f.read()


def initialized_environment():
    parent = os.path.dirname(__file__)
    # path = os.path.join(parent, 'templates')
    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(parent)
    # 用加载器创建一个环境, 有了它才能读取模板文件
    e = Environment(loader=loader)
    return e


class Template:
    e = initialized_environment()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        # 调用 get_template() 方法加载模板并返回
        
        template = cls.e.get_template(filename)
        # 用 render() 方法渲染模板
        # 可以传递参数
        return template.render(*args, **kwargs)


def save(file, data):
    with open(file, 'w') as f:
        f.write(data)


def gene_index():
    csss = [
        # # bootstrap
        load("templates/css/bootstrap.min.css"),
        load("templates/css/all.css"),
        # # bootstrap table
        load("templates/css/bootstrap-table.min.css"),
        # #  css alertify
        load("templates/css/alertify.min.css"),
        load("templates/css/default.min.css"),
        load("templates/css/semantic.min.css"),
        load("templates/css/bootstrap.min.css"),
        # #  pure css
        load("templates/css/pure-min.css"),
        # # css
        load("templates/css/raw.css"),
    ]
    scripts = [
        # 第三方库
        load("templates/js/jquery-3.3.1.min.js"),
        load("templates/js/popper.min.js"),
        load("templates/js/bootstrap.min.js"),
        load("templates/js/bootstrap-table.min.js"),
        load("templates/js/alertify.min.js"),
        load("templates/js/progressbar.js"),
        load("templates/js/table.js"),

        # 自定义脚本
        load("templates/js/raw.js"),
    ]
    r = Template.render('templates/template.html', scripts=scripts, csss=csss)
    save('templates/index.html', r)



if __name__ == "__main__":
    gene_index()
