from app import app,db
from app.product.models import Item

# results = Item.query(*[c for c in Item.query.all() if c.name != 'Ghiraula']).all()
results = [c for c in Item.query.all() if c.name != 'Ghiraula']

print(results)