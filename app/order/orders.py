from flask import session,flash,redirect,url_for,render_template,request,make_response
from flask_login import current_user
from app import app,db,login_required
from .models import CustomerOrder
from .forms import UpdateOrderByStaff
from app.user.models import User
import secrets
import pdfkit
from app.product.productutils import getCategoriesAndItems

def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']

    return updateshoppingcart

# +++++++++++++++++++++++++++++++++++ Customer ++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/makeorder')
@login_required(role="customer")
def make_order():
    if current_user.is_authenticated:
        id = current_user.id
        invoice_number = secrets.token_hex(5)
        updateshoppingcart
        try:
            order = CustomerOrder(invoice_number=invoice_number,customer_id=id,orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully','success')

            #TODO reduce left quantity after every order

            return redirect(url_for('orders',invoice_number=invoice_number))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while getting order', 'danger')
            return redirect(url_for('getCart'))

@app.route('/orders/<invoice_number>')
@login_required(role="customer")
def orders(invoice_number):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = User.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice_number=invoice_number).order_by(CustomerOrder.id.desc()).first()
        allcategories=[]
        allitems=[]
        try:
            allcategories , allitems = getCategoriesAndItems()
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = ("%.2f" % (.00 * float(subTotal)))
                grandTotal = ("%.2f" % (1.00 * float(subTotal)))
            return render_template('order/orderpage.html', invoice_number=invoice_number, tax=tax,subTotal=subTotal,grandTotal=grandTotal,customer=customer,orders=orders)
        except Exception as err:
            print(err)
            flash("No orders found!",'danger')
            return redirect(url_for('customer_home',allcategories=allcategories,allitems=allitems))
    else:
        return redirect(url_for('login'))
    
@app.route('/get_pdf/<invoice_number>', methods=['POST'])
@login_required(role="customer")
def get_pdf(invoice_number):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        if request.method =="POST":
            try:
                customer = User.query.filter_by(id=customer_id).first()
                orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice_number=invoice_number).order_by(CustomerOrder.id.desc()).first()
                for _key, product in orders.orders.items():
                    discount = (product['discount']/100) * float(product['price'])
                    subTotal += float(product['price']) * int(product['quantity'])
                    subTotal -= discount
                    tax = ("%.2f" % (.00 * float(subTotal)))
                    grandTotal = float("%.2f" % (1.00 * subTotal))
                rendered =  render_template('order/pdf.html', invoice_number=invoice_number, tax=tax,grandTotal=grandTotal,customer=customer,orders=orders)
                
                # pdffile = app.config['GENERATED_CUSTOMER_INVOICE_FOLDER'] + '/'+invoice_number+'.pdf'
                # pdffile = 'app/static/static/pdf/customer-invoices/'+invoice_number+'.pdf'
                pdf = pdfkit.from_string(rendered, False)
                
                response = make_response(pdf)
                response.headers['content-Type'] ='application/pdf'
                # to make client only view the pdf
                # response.headers['content-Disposition'] ='inline; filename='+invoice_number+'.pdf'
                
                # to make client download the pdf
                response.headers['content-Disposition'] ='attachment; filename='+invoice_number+'.pdf'
                return response
            except Exception as err:
                print(err)
                flash("Problem while reading pdf!",'danger')
                return redirect(url_for('customer_home'))

    return request(url_for('orders'))


@app.route('/thankyou')
@login_required(role="customer")
def thankyou():
    allcategories , allitems = getCategoriesAndItems()
    return render_template('order/thankyou.html',allcategories=allcategories)


@app.route('/customer/orders')
@login_required(role="customer")
def customer_orders():
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = User.query.filter_by(id=customer_id).first()
        allorders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).all()
        listofTupleDTG = []
        
        allcategories , allitems = getCategoriesAndItems()
        try:
            for eachorder in allorders:
                discount=0
                subTotal=0
                tax=0
                grandTotal=0
                for _key, product in eachorder.orders.items():
                    discount = (product['discount']/100) * float(product['price'])
                    subTotal += float(product['price']) * int(product['quantity'])
                    subTotal -= discount
                    tax = ("%.2f" % (.00 * float(subTotal)))
                    grandTotal = ("%.2f" % (1.00 * float(subTotal)))
                listofTupleDTG.append((eachorder.invoice_number,eachorder.status,eachorder.date_created,discount,tax,grandTotal))
            # print(listofTupleDTG)
            return render_template('customer/orders-all.html', listofTupleDTG=listofTupleDTG,allcategories=allcategories)
        except Exception as err:
            print(err)
            flash("No orders found!",'danger')
            return redirect(url_for('customer_home',allcategories=allcategories,allitems=allitems))

    else:
        return redirect(url_for('login'))
# +++++++++++++++++++++++++++++++++++ Customer ++++++++++++++++++++++++++++++++++++++++++++++++++++



# +++++++++++++++++++++++++++++++++++ Staff ++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/staff/orders')
@login_required(role="staff")
def getallorders_staff():

    allorders = CustomerOrder.query.order_by(CustomerOrder.id.desc()).all()
    listofTupleDTG = []
    try:
        for eachorder in allorders:
            discount=0
            subTotal=0
            tax=0
            grandTotal=0
            for _key, product in eachorder.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = ("%.2f" % (.00 * float(subTotal)))
                grandTotal = ("%.2f" % (1.00 * float(subTotal)))
            listofTupleDTG.append((eachorder.invoice_number,eachorder.status,eachorder.date_created,discount,tax,grandTotal,eachorder.id))
        print(listofTupleDTG)
        return render_template('staff/orders-all.html', listofTupleDTG=listofTupleDTG)
    except Exception as err:
        print(err)
        flash("No orders found!",'danger')
        return redirect(url_for('staff_home'))

@app.route('/staff/updateorder/<int:id>',methods=['GET','POST'])
@login_required(role="staff")
def updateorder_staff(id):
    form = UpdateOrderByStaff()
    try:
        order = CustomerOrder.query.get_or_404(id)
        if request.method =="POST":
            order.status = request.form.get('orderstatus')
            db.session.add(order)
            db.session.commit()
            flash(f'The status of order with invoice number {order.invoice_number} has been changed to {order.status}','success')
            return redirect(url_for('staff_home'))
        form=UpdateOrderByStaff(obj=order or None)
        return render_template('staff/order-update.html', title='Update Order',form=form,currentOrder=order)
    except Exception as err:
        print(err)
        flash(f'Some problem during the update','danger')
        return render_template('staff/order-update.htm', title='Update Order',form=form,currentOrder=order)

# +++++++++++++++++++++++++++++++++++ End Staff ++++++++++++++++++++++++++++++++++++++++++++++++