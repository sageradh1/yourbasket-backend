# from flask import render_template,session, request,redirect,url_for,flash,current_app
from flask import render_template,redirect,request,session,url_for,flash
from app import db , app
from app.product.models import Item
# import json

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

@app.route('/addtocart', methods=['POST'])
def addtocart():
    try:
        item_id = request.form.get('item_id')
        quantity = int(request.form.get('quantity'))
        item = Item.find_by_id(item_id)

        if request.method =="POST":
            DictItems = {item_id:{'name':item.name,'price':float(item.price),'discount':item.discount,'quantity':quantity,'left_quantity':item.left_quantity,'image':item.image_1}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if item_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(item_id):
                            session.modified = True
                            
                            if item['quantity']+ quantity > item['left_quantity']:
                                item['quantity']=item['left_quantity']
                            else:
                                item['quantity'] = item['quantity']+ quantity
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)    
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        flash("Cart is Empty",'danger')
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key,item in session['Shoppingcart'].items():
        if item['image'] is None:
            item['image']='no-image.png'
        discount = (item['discount']/100) * float(item['price'])
        subtotal += float(item['price']) * int(item['quantity'])
        subtotal -= discount
        # tax =("%.2f" %(.06 * float(subtotal)))
        tax=0
        grandtotal = float("%.2f" % (1.00 * subtotal))
    brands=[]
    categories=[]
    return render_template('cart/cart.html',tax=tax, grandtotal=grandtotal,brands=brands,categories=categories)


@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method =="POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key , item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated!')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))



@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key , item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))


@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
