from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitches = db.relationship('Pitch',backref = 'user',lazy="dynamic")
    upvotes = db.relationship('UpVote',backref = 'user',lazy="dynamic")
    downvotes = db.relationship('DownVote',backref = 'user',lazy="dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy="dynamic")
    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    text = db.Column(db.String(255))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    upvotes = db.relationship('UpVote',backref = 'pitch',lazy="dynamic")
    downvotes = db.relationship('DownVote',backref = 'pitch',lazy="dynamic")
    comments = db.relationship('Comment',backref = 'pitch',lazy="dynamic")

    def save_pitch(self):
        
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls):

        return Pitch.query.all()

    @classmethod
    def get_pitches_by_category(cls,category_id):
        
        return Pitch.query.filter_by(category_id= category_id)

    

class Category(db.Model):
    __tablename__= 'categories'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    pitches = db.relationship('Pitch',backref = 'category',lazy="dynamic")

    @classmethod
    def get_categories(cls):
        
        categories = Category.query.all()
        return categories

    def __repr__(self):
        return f'User {self.name}'

class UpVote(db.Model):
    __tablename__= 'upvotes'

    id = db.Column(db.Integer,primary_key = True)
    upvote = db.Column(db.Integer,default=1)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))

    def save_votes(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def add_upvotes(cls,id):
        upvote_pitch = UpVote(user = current_user, pitch_id=id)
        upvote_pitch.save_upvotes()

    @classmethod
    def get_votes(cls, id):
        upvote = UpVote.query.filter_by(pitch_id=id).all()
        return upvote

    def __repr__(self):
        return f'User {self.id}'

class DownVote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key = True)
    downvote = db.Column(db.Integer,default=1)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))

    def save_votes(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def add_downvotes(cls,id):
        downvote_pitch = DownVote(user = current_user, pitch_id=id)
        downvote_pitch.save_downvotes()

    @classmethod
    def get_votes(cls, id):
        downvote = DownVote.query.filter_by(pitch_id=id).all()
        return downvote

    def __repr__(self):
        return f'User {self.id}'

class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments

    def __repr__(self):
        return f'User {self.comment}'

