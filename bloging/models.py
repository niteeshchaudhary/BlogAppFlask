from bloging import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('blogs', lazy=True))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.relationship('User', secondary='likes', backref=db.backref('liked_blogs', lazy='dynamic'))

    def __repr__(self):
        return f'<Blog {self.id}>'

likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('blog_id', db.Integer, db.ForeignKey('blogs.id'), primary_key=True)
)
    