from flask import Flask,render_template, render_template_string
import markdown
app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/md')
def servemd():
    with open("README.md") as md_file:
        md_content = md_file.read()
        html_content = markdown.markdown(md_content)
        return render_template_string('<html><body>{{ content | safe }}</body></html>', content=html_content)
    