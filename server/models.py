from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    

    @validates('name')
    def validate_author_name(self, key, name):
        # Check if the instance is in the session (already added or to be added)
        existing_author = db.session.query(Author).filter(Author.name == name).first()

        # If the instance is not in the session, check the database for existing authors
        if not db.object_session(self):
            if existing_author:
                raise ValueError("Another author with the same name already exists.")
            
        if not name:
            raise ValueError("Author must have a name.")

        return name

    @validates('phone_number')
    def validate_author_phone_number(self, key, phone_number):
        if phone_number and not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Author phone numbers must be exactly ten digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_post_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_post_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters.")
        return summary

    @validates('category')
    def validate_post_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'.")
        return category

    @validates('title')
    def validate_post_title(self, key, title):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError("Post title must be sufficiently clickbait-y.")
        return title 


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
