import datetime
import io
import json
import os

#from feedgen.feed import FeedGenerator
from flask import Flask, render_template, request, redirect, Response, send_file, abort
from flask_mail import Mail

app = Flask(__name__)
mail = Mail(app)

try:
    app.config['GA_TRACKING_ID'] = os.environ['GA_TRACKING_ID']
except:
    print('Tracking ID not set')

resume_pdf_link = 'https://docs.google.com/document/d/14GalBEZfrcRyqGa_E2yxnoLpRsnHTojCei5jBAT2s0A/edit?usp=sharing'


@app.route('/')
def index():
    age = int((datetime.date.today() - datetime.date(1995, 4, 22)).days / 365)
    return render_template('home.html', age=age)


@app.route('/projects')
def projects():
    data = get_static_json("static/projects/projects.json")['projects']
    data.sort(key=order_projects_by_weight, reverse=True)

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template('projects.html', projects=data, tag=tag)

@app.route('/experiences')
def experiences():
    experiences = get_static_json("static/experiences/experiences.json")['experiences']
    experiences.sort(key=order_projects_by_weight, reverse=True)
    return render_template('experiences.html', projects=experiences, tag=None)

@app.route('/dogs')
def dogs():
    dogs = get_static_json("static/dogs/dogs.json")['dogs']
    dogs.sort(key=order_projects_by_weight, reverse=True)
    return render_template('dogs.html', projects=dogs, tag=None)

@app.route('/woods')
def woods():
    woods = get_static_json("static/woods/woods.json")['woods']
    woods.sort(key=order_projects_by_weight, reverse=True)
    return render_template('woods.html', projects=woods, tag=None)

@app.route('/gardens')
def gardens():
    gardens = get_static_json("static/gardens/gardens.json")['gardens']
    gardens.sort(key=order_projects_by_weight, reverse=True)
    return render_template('gardens.html', projects=gardens, tag=None)

def order_projects_by_weight(projects):
    try:
        return int(projects['weight'])
    except KeyError:
        return 0


@app.route('/projects/<title>')
def project(title):
    projects = get_static_json("static/projects/projects.json")['projects']
    experiences = get_static_json("static/experiences/experiences.json")['experiences']

    in_project = next((p for p in projects if p['link'] == title), None)
    in_exp = next((p for p in experiences if p['link'] == title), None)

    if in_project is None and in_exp is None:
        return render_template('404.html'), 404
    # fixme: choose the experience one for now, cuz I've done some shite hardcoding here.
    elif in_project is not None and in_exp is not None:
        selected = in_exp
    elif in_project is not None:
        selected = in_project
    else:
        selected = in_exp

    # load html if the json file doesn't contain a description
    if 'description' not in selected:
        path = "experiences" if in_exp is not None else "projects"
        selected['description'] = io.open(get_static_file(
            'static/%s/%s/%s.html' % (path, selected['link'], selected['link'])), "r", encoding="utf-8").read()
    if in_exp:
        return render_template('experience.html', project=selected)
    return render_template('project.html', project=selected)


@app.route('/resume')
def resume():
    #return redirect(resume_pdf_link, code=302)
    return render_template("resume.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)


def get_static_json(path):
    return json.load(open(get_static_file(path)))


if __name__ == "__main__":
    print("running py app")
    app.run(host="127.0.0.1", port=5000, debug=True)
