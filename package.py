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
        raw_js=load("templates/raw.js"),
        raw_css=load("templates/raw.css"),
    )
    # save('templates/index.html', r)
    page = Template.render("templates/page.py", p=r)
    save('page.py', page)


if __name__ == "__main__":
    gene_index()
