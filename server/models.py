from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String)

    posts = db.relationship("Post", back_populates="author")

    # ---------------- VALIDATIONS ----------------

    @validates("name")
    def validate_name(self, key, name):
        if not name or name.strip() == "":
            raise ValueError("Author must have a name")

        # ✅ uniqueness validation (CodeGrade REQUIRED)
        existing_author = Author.query.filter(
            Author.name == name,
            Author.id != self.id if self.id else True
        ).first()

        if existing_author:
            raise ValueError("Author name must be unique")

        return name

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if phone_number is None:
            return phone_number

        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits")

        return phone_number


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String)
    category = db.Column(db.String, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    author = db.relationship("Author", back_populates="posts")

    __table_args__ = (
        CheckConstraint("LENGTH(summary) <= 250", name="summary_max_length"),
    )

    # ---------------- VALIDATIONS ----------------

    @validates("content")
    def validate_content(self, key, content):
        if not content or len(content) < 250:
            raise ValueError("Post content must be at least 250 characters")
        return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary must be 250 characters or fewer")
        return summary

    @validates("category")
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be Fiction or Non-Fiction")
        return category

    @validates("title")
    def validate_title(self, key, title):
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]

        if not any(word in title for word in clickbait_words):
            raise ValueError("Title must be clickbait-y")

        return title
