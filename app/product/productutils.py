from app.product.models import Item,Category

def unnullifystring(allitems):
    for eachitem in allitems:
        if eachitem.image_1 is None:
            eachitem.image_1="no-image.png"
        if eachitem.image_2 is None:
            eachitem.image_2="no-image.png"
        if eachitem.image_3 is None:
            eachitem.image_3="no-image.png"
    return allitems

def getCategoriesAndItems():
    return Category.get_all(),unnullifystring(Item.query.all())