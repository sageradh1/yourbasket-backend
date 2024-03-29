# from app import db
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
# from app import login

# class Admin(db.Model):
#     id = db.Column(db.Integer, primary_key=True)

#     email = db.Column(db.String(120), index=True, unique=True,nullable=True)
#     username = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(200))

#     contactnumber1 = db.Column(db.String(15))
#     contactnumber2 = db.Column(db.String(15))
    
#     def set_password(self, password):
#         """Create hashed password."""
#         self.password_hash = generate_password_hash(password, method='sha256')

#     def check_password(self, password):
#         """Check hashed password."""
#         return check_password_hash(self.password_hash, password)
        
#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()

#     @classmethod
#     def find_by_id(cls, _id):
#         return cls.query.filter_by(id=_id).first()

#     @classmethod
#     def find_by_username(cls, _username):
#         return cls.query.filter_by(username=_username).first()

#     def __repr__(self):
#         return '<User id:{} username:{} email:{}>'.format(self.id,self.username,self.email)

# db.create_all()