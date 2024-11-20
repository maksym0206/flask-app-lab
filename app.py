from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import redirect

app = Flask(__name__)
app.config.from_pyfile("config.py")


@app.route('/')  # URL '/' to be handled by main() route handler
def main():
    return redirect(url_for('resume'))


@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return f"<h1>This is your homepage :) - {agent}</h1> "


@app.route('/hi/<string:name>') #/hi/Andriy?age=20
def greetings(name):
    name = name.upper()
    age = request.args.get("age", 0, type=int)
    return f"Welcome {name=} {age=}", 200

@app.route('/admin')
def admin():
   to_url = url_for("greetings", name="Administrator", _external=True)            #"/hi/admin"
   print(to_url)
   return redirect(to_url)

@app.route('/resume')
def resume():
    return render_template('resume.html', title="Резюме")


if __name__ == "__main__":
    app.run()  # Launch built-in web server and run this Flask webapp, debug=True


