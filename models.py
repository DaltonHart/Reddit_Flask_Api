from app import db, marshmallow
from flask import jsonify


class Sub(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(300))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def create_sub(cls, name, description):
        new_sub = Sub(name, description)
        try:
            db.session.add(new_sub)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return sub_schema.jsonify(new_sub)

    @classmethod
    def get_sub(cls, subid):
        sub = Sub.query.get(subid)
        return sub_schema.jsonify(sub)

    @classmethod
    def get_subs(cls):
        subs = Sub.query.all()
        return subs_schema.jsonify(subs)


class SubSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


sub_schema = SubSchema()
subs_schema = SubSchema(many=True)


class Post(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    text = db.Column(db.String(500))
    user = db.Column(db.String(100))
    sub = db.Column(db.Integer, db.ForeignKey("sub.id"))

    def __init__(self, title, text, user, sub):
        self.title = title
        self.text = text
        self.user = user
        self.sub = sub

    @classmethod
    def create_post(cls, title, text, user, sub):
        new_post = Post(title, text, user, sub)
        try:
            db.session.add(new_post)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return post_schema.jsonify(new_post)

    @classmethod
    def get_post(cls, postid):
        post = Post.query.get(postid)
        return post_schema.jsonify(post)

    @classmethod
    def get_posts(cls):
        posts = Post.query.all()
        return posts_schema.jsonify(posts)

    @classmethod
    def filter_posts_by_sub(cls, subid):
        posts = Post.query.filter_by(sub=subid)
        return posts_schema.jsonify(posts)

    @classmethod
    def update_post(cls, postid, title=None, text=None):
        post = Post.query.get(postid)
        if title != None:
            post.title = title
        if text != None:
            post.text = text
        db.session.commit()
        return post_schema.jsonify(post)

    @classmethod
    def delete_post(cls, postid):
        post = Post.query.get(postid)
        db.session.delete(post)
        db.session.commit()
        return post_schema.jsonify(post)


class PostSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'title', 'text', 'user', 'sub')


post_schema = PostSchema()
posts_schema = PostSchema(many=True)

if __name__ == 'models':
    db.create_all()
