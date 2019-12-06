import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'sqlite:///' + os.path.join(basedir, 'db.reddit')
# DATABASE = 'postgresql://localhost/reddit'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
marshmallow = Marshmallow(app)

DEBUG = True
PORT = 8000


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/name')
@app.route('/name/<name_param>')
def name(name_param=None):
    if name_param == None:
        return "No name provided"
    return f"Hello, {name_param}"


@app.route('/sub', methods=['POST', 'GET'])
@app.route('/sub/<subid>', methods=['GET'])
def get_or_create_sub(subid=None):
    from models import Sub
    if subid == None and request.method == 'GET':
        return Sub.get_subs()
    elif subid == None:
        name = request.json['name']
        description = request.json['description']
        return Sub.create_sub(name, description)
    else:
        return Sub.get_sub(subid)


@app.route('/sub/<subid>/posts', methods=['GET'])
def get_sub_posts(subid):
    from models import Post
    return Post.filter_posts_by_sub(subid)


@app.route('/post', methods=['POST', 'GET'])
@app.route('/post/<postid>', methods=['GET'])
def get_or_create_post(postid=None):
    from models import Post
    if postid == None and request.method == 'GET':
        return Post.get_posts()
    elif postid == None:
        title = request.json['title']
        text = request.json['text']
        user = request.json['user']
        sub = request.json['sub']
        return Post.create_post(title, text, user, sub)
    else:
        return Post.get_post(postid)


@app.route('/post/<postid>', methods=['PUT', 'DELETE'])
def update_or_delete_post(postid=None):
    from models import Post
    if request.method == 'PUT':
        req = request.get_json()
        return Post.update_post(postid, **req)
    else:
        return Post.delete_post(postid)


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
