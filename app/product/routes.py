from flask import render_template,request,redirect,url_for,flash
# from shop import app,db,photos, search
from .models import Item,Category
from app import app,login_required,photos,db
from .productutils import getCategoriesAndItems,unnullifystring
from .forms import Additems,Addcategories,Updateitems
import os
from wtforms import SelectField
    
# ++++++++++++++++++++++++++++++++++++ Item +++++++++++++++++++++++++++++++++++++++++++++ 
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

############## Admin ############## 
@app.route('/admin/items/')
@login_required(role="admin")
def getallitems_admin():
    allcategories=[]
    allitems=[]
    try:
        allcategories , allitems = getCategoriesAndItems()
        return render_template('admin/items-all.html',allitems=allitems,allcategories=allcategories)
    except Exception as err:
        return render_template('admin/items-all.html',allitems=allitems,allcategories=allcategories)


@app.route('/additem', methods=['GET','POST'])
@login_required(role="admin")
def additem():
    IDS = [(each.id,each.name) for each in Category.query.all()]   
    # return IDS_CATEGORIES
    form = Additems()
    form.category_id_form.choices= IDS
    # form.category_id = SelectField('Category', choices=IDS,coerce=int)

    if request.method=="POST":
        try:
            if form.validate_on_submit():
                name = form.name.data
                price = form.price.data
                discount = form.discount.data
                left_quantity = form.left_quantity.data
                desc = form.desc.data
                category_id_form = request.form.get('category_id_form')
                quantity_measuring_unit = request.form.get('quantity_measuring_unit')
                
                image_1 = photos.save(request.files.get('image_1'), name=request.files.get('image_1').filename)
                # request.files.get('image_1').save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image_1))   
                
                if request.files.get('image_2'):
                    image_2 = photos.save(request.files.get('image_2'), name=request.files.get('image_2').filename)
                    # request.files.get('image_2').save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image_2))            
                else:
                    image_2 = app.config["DEFAULT_PHOTO_FOR_ITEMS"]
                
                if request.files.get('image_3'):
                    image_3 = photos.save(request.files.get('image_3'), name=request.files.get('image_3').filename)
                    # request.files.get('image_3').save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image_3))
                else:
                    image_3 = app.config["DEFAULT_PHOTO_FOR_ITEMS"]

                newItem = Item(name=name,price=price,discount=discount,left_quantity=left_quantity,desc=desc,quantity_measuring_unit=quantity_measuring_unit,category_id=category_id_form,image_1=image_1,image_2=image_2,image_3=image_3)
                db.session.add(newItem)
                flash(f'The product {name} was added in database','success')
                db.session.commit()
                return redirect(url_for('admin_home'))
            else:
                print("validation error")
                print(form.errors)
                return render_template('admin/item-add.html', form=form, title='Add a Product')
        except Exception as err:
            print(err)
            return render_template('admin/item-add.html', form=form, title='Add a Product')
    return render_template('admin/item-add.html', form=form, title='Add a Product')


@app.route('/updateitem/<int:id>', methods=['GET','POST'])
@login_required(role="admin")
def updateitem(id):

    IDS = [(each.id,each.name) for each in Category.query.all()]
    print(IDS)
    form = Updateitems()
    form.category_id_form.choices= IDS
    form.coerce=int
    
    item = Item.query.get_or_404(id)
    
    if request.method=="POST":
        try:
            # form = Updateitems()
            if form.validate_on_submit():
                
                item.name = form.name.data
                item.price = form.price.data
                item.discount = form.discount.data
                item.left_quantity = form.left_quantity.data
                item.desc = form.desc.data
                item.category_id = request.form.get('category_id_form')
                print(request.form.get('category_id_form'))
                item.quantity_measuring_unit = request.form.get('quantity_measuring_unit')
                
                if request.files.get('image_1'):
                    image_1 = photos.save(request.files.get('image_1'), name=request.files.get('image_1').filename)
                    item.image_1 = image_1
                    # request.files.get('image_2').save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image_2))            


                if request.files.get('image_2'):
                    image_2 = photos.save(request.files.get('image_2'), name=request.files.get('image_2').filename)
                    item.image_2 = image_2
                    # request.files.get('image_2').save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image_2))            

                
                if request.files.get('image_3'):
                    image_3 = photos.save(request.files.get('image_3'), name=request.files.get('image_3').filename)
                    item.image_3 = image_3
                    # request.files.get('image_3').save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image_3))

                db.session.add(item)
                flash(f'The product was updated in database','success')
                db.session.commit()
                return redirect(url_for('admin_home'))

            else:
                print(form.errors)
                flash('Problem while updating item','warning')
                form = Updateitems(obj=item or None)
                form.category_id_form.choices= IDS
                return render_template('admin/item-add.html', form=form, title='Update Product',currentItem=item)

        except Exception as err:
            print(err)
            form = Updateitems(obj=item or None)
            form.category_id_form.choices= IDS
            return render_template('admin/item-add.html', form=form, title='Update Product',currentItem=item)
    
    form = Updateitems(obj=item or None)
    form.category_id_form.choices= IDS
    form.coerce=int
    return render_template('admin/item-add.html', form=form, title='Update Product',currentItem=item)


@app.route('/deleteitem/<int:id>', methods=['POST'])
@login_required(role="admin")
def deleteitem(id):
    try:
        item = Item.query.get_or_404(id)
        if request.method=="POST":
            db.session.delete(item)
            db.session.commit()
            flash(f"Requested product was deleted from your database","success")
            return redirect(url_for('admin_home'))
        flash(f"Error while deleting product","warning")
    except Exception as err:
        print(err)
        flash(f"Error while deleting product","warning")

############## Admin End ##############


############## Staff End ##############
@app.route('/staff/items/')
@login_required(role="staff")
def getallitems_staff():
    allcategories=[]
    allitems=[]
    try:
        allcategories , allitems = getCategoriesAndItems()
        return render_template('staff/items-all.html',allitems=allitems,allcategories=allcategories)
    except Exception as err:
        return render_template('staff/items-all.html',allitems=allitems,allcategories=allcategories)
############## Staff End ##############
# ++++++++++++++++++++++++++++++++++++End Item +++++++++++++++++++++++++++++++++++++++++++++ 

# ++++++++++++++++++++++++++++++++++++ Categories +++++++++++++++++++++++++++++++++++++++++++++ 
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

############## Admin ##############
@app.route('/admin/categories/')
@login_required(role="admin")
def getallcategories_admin():
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
@login_required(role="admin")
def updatecategory(id):
    form = Addcategories()
    try:
        cat = Category.query.get_or_404(id)
        oldname = cat.name
        newname = request.form.get('name')  
        if request.method =="POST":
            cat.name = newname
            db.session.add(cat)
            db.session.commit()
            flash(f'The category {oldname} was changed to {newname}','success')
            return redirect(url_for('admin_home'))
        form=Addcategories(obj=cat or None)
        return render_template('admin/category-add.html', title='Update Category',form=form,getCat=cat)
    except Exception as err:
        print(err)
        flash(f'Some problem during the update','danger')
        return render_template('admin/category-add.html', title='Update Category',form=form,getCat=cat)

@app.route('/deletecategory/<int:id>', methods=['GET','POST'])
@login_required(role="admin")
def deletecategory(id):
    try:
        category = Category.query.get_or_404(id)
        if request.method=="POST":
            db.session.delete(category)
            db.session.commit()
            flash(f"Requested category was deleted from your database","success")
            return redirect(url_for('admin_home'))
        flash(f"Error while deleting category","warning")
    except Exception as err:
        print(err)
        flash(f"Error while deleting category","warning")
############## Admin End ##############


############## Staff ##############
@app.route('/staff/categories/')
@login_required(role="staff")
def getallcategories_staff():
    allcategories=[]
    allitems=[]
    try:
        allcategories , allitems = getCategoriesAndItems()
        return render_template('staff/categories-all.html',allcategories=allcategories)
    except Exception as err:
        return render_template('staff/categories-all.html',allcategories=allcategories)
############## Staff End ##############
# ++++++++++++++++++++++++++++++++++++ Category End +++++++++++++++++++++++++++++++++++++++++++++ 

# ++++++++++++++++++++++++++++++++++++ Product search +++++++++++++++++++++++++++++++++++++++++++++      
@app.route('/result')
def result():
    allcategories , allitems = getCategoriesAndItems()
    searchword = request.args.get('q')
    selected_items = Item.query.msearch(searchword, fields=['name','desc'] , limit=16)
    return render_template('product/items_search_result.html',selected_items=selected_items,allcategories=allcategories)
