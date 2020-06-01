from flask import session,flash,redirect,url_for,render_template,request,make_response
from flask_login import login_required,current_user
from app import app,db
from .models import CustomerOrder
from app.customer.models import User
import secrets
import pdfkit

def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']
        del shopping['colors']
    return updateshoppingcart

@app.route('/makeorder')
@login_required
def make_order():
    if current_user.is_authenticated:
        id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart
        try:
            order = CustomerOrder(invoice_number=invoice,id=id,orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully','success')
            return redirect(url_for('orders',invoice_number=invoice_number))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while getting order', 'danger')
            return redirect(url_for('getCart'))

@app.route('/orders/<invoice_number>')
@login_required
def orders(invoice_number):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = User.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice_number=invoice_number).order_by(CustomerOrder.id.desc()).first()
        
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            tax = ("%.2f" % (.00 * float(subTotal)))
            grandTotal = ("%.2f" % (1.00 * float(subTotal)))
    else:
        return redirect(url_for('customer_login'))
    return render_template('order/orderpage.html', invoice_number=invoice_number, tax=tax,subTotal=subTotal,grandTotal=grandTotal,customer=customer,orders=orders)

@app.route('/get_pdf/<invoice_number>', methods=['POST'])
@login_required
def get_pdf(invoice_number):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        if request.method =="POST":
            customer = User.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice_number=invoice_number).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = ("%.2f" % (.00 * float(subTotal)))
                grandTotal = float("%.2f" % (1.00 * subTotal))

            rendered =  render_template('order/pdf.html', invoice_number=invoice_number, tax=tax,grandTotal=grandTotal,customer=customer,orders=orders)
            pdffile = app.config['GENERATED_CUSTOMER_INVOICE_FOLDER'] + '/'+invoice_number+'.pdf'
            pdf = pdfkit.from_string(rendered, pdffile)
            response = make_response(pdf)
            response.headers['content-Type'] ='application/pdf'
            # to make client only view the pdf
            # response.headers['content-Disposition'] ='inline; filename='+invoice_number+'.pdf'
            
            # to make client download the pdf
            response.headers['content-Disposition'] ='attachment; filename='+invoice_number+'.pdf'

            return response
    return request(url_for('orders'))


@app.route('/thanks')
def thanks():
    return render_template('order/thank.html')