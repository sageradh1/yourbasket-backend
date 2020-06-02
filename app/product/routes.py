from flask import render_template,request,redirect,url_for,flash
# from shop import app,db,photos, search
from .models import Item,Category
from app import app,login_required,photos,db
from .productutils import getCategoriesAndItems,unnullifystring
from .forms import Additems,Addcategories
import os
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

@app.route('/admin/items/')
@login_required(role="admin")
def getallitems_admin(id):
    allcategories=[]
    allitems=[]
    try:
        allcategories , allitems = getCategoriesAndItems()
        return render_template('admin/items-all.html',allitems=allitems)
    except Exception as err:
        
        return render_template('admin/items-all.html',allitems=allitems)


@app.route('/additem', methods=['GET','POST'])
@login_required(role="admin")
def additem():
    form = Additems()

    if request.method=="POST":
        try:
            if form.validate_on_submit():
                name = form.name.data
                price = form.price.data
                discount = form.discount.data
                left_quantity = form.left_quantity.data
                desc = form.description.data
                category_id = request.form.get('category_id')
                quantity_measuring_unit = request.form.get('quantity_measuring_unit')
                
                image_1 = photos.save(request.files.get('image_1'), name=request.files.get('image_1').filename)
                request.files.get('image_1').save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image_1))   
                
                if request.files.get('image_2'):
                    image_2 = photos.save(request.files.get('image_2'), name=request.files.get('image_2').filename)
                    request.files.get('image_2').save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image_2))            
                else:
                    image_2 = app.config["DEFAULT_PHOTO_FOR_ITEMS"]
                
                if request.files.get('image_3'):
                    image_3 = photos.save(request.files.get('image_3'), name=request.files.get('image_3').filename)
                    request.files.get('image_3').save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image_3))
                else:
                    image_3 = app.config["DEFAULT_PHOTO_FOR_ITEMS"]

                newItem = Item(name=name,price=price,discount=discount,left_quantity=left_quantity,desc=desc,quantity_measuring_unit=quantity_measuring_unit,category_id=category_id,image_1=image_1,image_2=image_2,image_3=image_3)
                db.session.add(newItem)
                flash(f'The product {name} was added in database','success')
                db.session.commit()
                return redirect(url_for('admin_home'))

            else:
                print(form.errors)
                return render_template('admin/item-add.html', form=form, title='Add a Product')

        except Exception as err:
            print(err)
            return render_template('admin/item-add.html', form=form, title='Add a Product')

        
    return render_template('admin/item-add.html', form=form, title='Add a Product')


@app.route('/updateitem/<int:id>', methods=['GET','POST'])
@login_required(role="admin")
def updateitem(id):
#     form = Addproducts(request.form)
#     product = Addproduct.query.get_or_404(id)
#     brands = Brand.query.all()
#     categories = Category.query.all()
#     brand = request.form.get('brand')
#     category = request.form.get('category')
#     if request.method =="POST":
#         product.name = form.name.data 
#         product.price = form.price.data
#         product.discount = form.discount.data
#         product.stock = form.stock.data 
#         product.colors = form.colors.data
#         product.desc = form.discription.data
#         product.category_id = category
#         product.brand_id = brand
#         if request.files.get('image_1'):
#             try:
#                 os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
#                 product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
#             except:
#                 product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
#         if request.files.get('image_2'):
#             try:
#                 os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
#                 product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
#             except:
#                 product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
#         if request.files.get('image_3'):
#             try:
#                 os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
#                 product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
#             except:
#                 product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

#         flash('The product was updated','success')
#         db.session.commit()
#         return redirect(url_for('admin'))
#     form.name.data = product.name
#     form.price.data = product.price
#     form.discount.data = product.discount
#     form.stock.data = product.stock
#     form.colors.data = product.colors
#     form.discription.data = product.desc
#     brand = product.brand.name
#     category = product.category.name
#     return render_template('products/addproduct.html', form=form, title='Update Product',getproduct=product, brands=brands,categories=categories)
    return 'updateitem'

@app.route('/deleteitem/<int:id>', methods=['POST'])
@login_required(role="admin")
def deleteitem(id):
#     product = Addproduct.query.get_or_404(id)
#     if request.method =="POST":
#         try:
#             os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
#             os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
#             os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
#         except Exception as e:
#             print(e)
#         db.session.delete(product)
#         db.session.commit()
#         flash(f'The product {product.name} was delete from your record','success')
#         return redirect(url_for('adim'))
#     flash(f'Can not delete the product','success')
#     return redirect(url_for('admin'))
    return 'delete'





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


@app.route('/admin/categories/')
@login_required(role="admin")
def getallcategories_admin(id):
    allcategories=[]
    allitems=[]
    try:
        allcategories , allitems = getCategoriesAndItems()
        return render_template('admin/categories-all.html',allcategories=allcategories)
    except Exception as err:
        
        return render_template('admin/categories-all.html',allcategories=allcategories)



@app.route('/addcategory', methods=['GET','POST'])
@login_required(role="admin")
def addcategory():
    form = Addcategories()

    if request.method=="POST":
        try:
            if form.validate_on_submit():
                name = form.name.data
 
                newCategory = Category(name=name)
                db.session.add(newCategory)
                flash(f'The category {name} was added in database','success')
                db.session.commit()
                return redirect(url_for('admin_home'))

            else:
                print(form.errors)
                return render_template('admin/category-add.html', form=form, title='Add a Category')

        except Exception as err:
            print(err)
            return render_template('admin/category-add.html', form=form, title='Add a Category')

        
    return render_template('admin/category-add.html', form=form, title='Add a Category')


@app.route('/updatecategory/<int:id>',methods=['GET','POST'])
def updatecategory(id):
    # if 'email' not in session:
    #     flash('Login first please','danger')
    #     return redirect(url_for('login'))
    # updatecat = Category.query.get_or_404(id)
    # category = request.form.get('category')  
    # if request.method =="POST":
    #     updatecat.name = category
    #     flash(f'The category {updatecat.name} was changed to {category}','success')
    #     db.session.commit()
    #     return redirect(url_for('categories'))
    # category = updatecat.name
    # return render_template('products/addbrand.html', title='Update cat',updatecat=updatecat)
    return 'updatecart'



@app.route('/deletecategory/<int:id>', methods=['GET','POST'])
def deletecategory(id):
    # category = Category.query.get_or_404(id)
    # if request.method=="POST":
    #     db.session.delete(category)
    #     flash(f"The brand {category.name} was deleted from your database","success")
    #     db.session.commit()
    #     return redirect(url_for('admin'))
    # flash(f"The brand {category.name} can't be  deleted from your database","warning")
    return 'deletcart'

#################################### Product Search #################################################
        
@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Item.query.msearch(searchword, fields=['name','desc'] , limit=16)
    return render_template('products/result.html',products=products,brands=brands(),categories=categories())
