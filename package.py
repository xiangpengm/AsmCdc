import os
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
    # print("path", path)
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
    r = Template.render("templates/template.html", 
        # js
        raw_js=load("templates/js/raw.js"),
        table_js=load("templates/js/table.js"),
        alertify_js=load("templates/js/alertify.min.js"),
        progressbar_js=load("templates/js/progressbar.js"),
        # css
        raw_css=load("templates/css/raw.css"),
        pure_css=load("templates/css/pure-min.css"),
        #  css alertify
        alertify_css=load("templates/css/alertify.min.css"),
        default_css=load("templates/css/default.min.css"),
        semantic_css=load("templates/css/semantic.min.css"),
        bootstrap_css=load("templates/css/bootstrap.min.css"),

    )
    page = Template.render("templates/page.py", p=r)
    save('templates/index.html', r)
    save('page.py', page)


if __name__ == "__main__":
    gene_index()
