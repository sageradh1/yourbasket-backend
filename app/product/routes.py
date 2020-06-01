from flask import render_template,request
# from shop import app,db,photos, search
from .models import Item,Category
from app import app
from .productutils import getCategoriesAndItems,unnullifystring

################################ Item ################################################### 
@app.route('/item/<int:id>')
def item_details_page(id):
    allcategories=[]
    allitems=[]
    try:
        allcategories , allitems = getCategoriesAndItems()
        item = Item.find_by_id(id)
        return render_template('product/items_details.html',item=item,allcategories=allcategories,allitems=allitems)
    except Exception as err:
        product = Item.get_empty_item()
        return render_template('product/items_details.html',item=item,allcategories=allcategories,allitems=allitems)



################################ Categories ###################################################
@app.route('/categories/<int:id>')
def get_category(id):
    allcategories=[]
    allitems=[]
    try:
        allcategories , allitems = getCategoriesAndItems()
        #how many items per page
        number_of_itemsperpage=8

        page = request.args.get('page',1, type=int)
        cat = Category.find_by_id(id)
        get_cat_product = Item.query.filter_by(category_id=id).paginate(page=page, per_page=number_of_itemsperpage)
        unnullifystring(get_cat_product.items)
        return render_template('product/items_in_category.html',get_cat_prod=get_cat_product,number_of_itemsperpage=number_of_itemsperpage,get_cat=cat,allcategories=allcategories,allitems=allitems)

    except Exception as err:
        print(err)
        return render_template('product/items_in_category.html',get_cat_prod=get_cat_product,number_of_itemsperpage=number_of_itemsperpage,get_cat=cat,allcategories=allcategories,allitems=allitems)

#################################### Product Search #################################################
        
@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Item.query.msearch(searchword, fields=['name','desc'] , limit=6)
    return render_template('products/result.html',products=products,brands=brands(),categories=categories())
