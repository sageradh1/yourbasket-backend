from app import db
from datetime import datetime


class Item(db.Model):
    __seachbale__ = ['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    left_quantity = db.Column(db.Integer, nullable=False)
    quantity_measuring_unit = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.Text)
    
    category_id = db.Column(db.Integer,nullable=False)
    
    image_1 = db.Column(db.String(150), default='image1.jpg')
    image_2 = db.Column(db.String(150), default='image2.jpg')
    image_3 = db.Column(db.String(150), default='image3.jpg')

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get_or_404(_id)
    
    @classmethod
    def find_all_by_category_id(cls, _id):
        return cls.query.filter_by(category_id=_id).all()

    def get_empty_item():
        newItem = Item()
        newItem.name = ""
        newItem.price = 0
        newItem.discount = 0
        newItem.left_quantity = 0
        newItem.quantity_measuring_unit = "unit"
        newItem.desc = ""
        newItem.category_id = -1
        newItem.image_1 = "image1.jpg"
        return newItem

    def __repr__(self):
        return '<Item %r price %r left %r%r categoryid %r >' % self.name,str(self.price),str(self.left_quantity),self.quantity_measuring_unit,self.category_id
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def get_empty_category():
        newItem = Category()
        newItem.name = ""
        return newItem

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, _name):
        return cls.query.filter_by(name=_name).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def __repr__(self):
        return '<Catgory %r>' % self.name

