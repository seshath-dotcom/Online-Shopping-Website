import streamlit as st
import mysql.connector

con = mysql.connector.connect(host="localhost",user="root",password="12345",database="inventory_management")
res = con.cursor()



def signup():
    fname,lname=st.columns(2)
    first_name=fname.text_input("First name",placeholder="Enter your first name")
    last_name=lname.text_input("Last name",placeholder="Enter your last name")
    
    mail,ph=st.columns([2,1])
    email=mail.text_input("Email",placeholder="Enter your Email")
    phone=ph.text_input("Phone number",placeholder="Enter your Phone number")

    user_name=st.text_input("Username",placeholder="choose your user name")
    
    pwsd,pwsd1=st.columns(2)
    
    pwd=pwsd.text_input("Password",placeholder="Choose your password")
    re_password=pwsd1.text_input("Re-Password",placeholder="Re-Enter the password")
    
    bt=st.button("Submit")

    usernames=[]
    qry = "select user_name from customer_details"
    res.execute(qry)
    data = res.fetchall()
    con.commit()
    for i in data:
        usernames.append(i[0])
    
    if bt:
        if user_name in usernames:
            st.warning("User name already exist")
        elif pwd!=re_password:
            st.warning("Password mismatch")
        else:
            st.info("successfull")
            qry = "insert into customer_details (first_name,last_name,email,phone,user_name,pwd) values (%s,%s,%s,%s,%s,%s)"
            val = (first_name,last_name,email,phone,user_name,pwd)
            res.execute(qry,val)
            con.commit()



def get_customer_ids():
    customer_ids=[]
    qry = "select customer_id from customer"
    res.execute(qry)
    data = res.fetchall()
    con.commit()
    for i in data:
        customer_ids.append(i[0])
    return customer_ids

def get_product_ids():
    product_ids=[]
    qry = "select product_id from product_details"
    res.execute(qry)
    data = res.fetchall()
    con.commit()
    for i in data:
        product_ids.append(i[0])
    return product_ids
    
def show_products():
    qry = "select product_id,product_name,price from product_details"
    res.execute(qry)
    data = res.fetchall()
    con.commit()
    product=[]
    price=[]
    product_id=[]
    for i in data:
        product_id.append(i[0])
        product.append(i[1])
        price.append(i[2])
    
    datum={"Product Id":product_id,"Product Name":product,"Price":price}
    st.dataframe(datum)

def stock_update():
    product_name=input("Enter the product name")
    stock_quantity=int(input("Enter the stock quantity"))
    price=int(input("Enter the price"))
    qry = "insert into product_details (product_name,stock_quantity,price) values (%s,%s,%s)"
    val = (product_name,stock_quantity,price)
    res.execute(qry,val)
    con.commit()

def new_order():
    user_name=st.text_input("User Name",placeholder="Enter your User Name")
    show_products()
    
    product_id=st.text_input("product_id",placeholder="Enter the product id you want to order")
    
        
    quantity=st.number_input("Quantity",placeholder="Enter the number of quantity",value=0,step=1)
        
        #getting customer_id
    slt=st.checkbox("Submit")
    if slt:
        
        qry = "select customer_id from customer_details where user_name=%s"
        res.execute(qry,(user_name,))
        dat=res.fetchall()
        con.commit()
        customer_id=dat[0][0]

        #getting stock_details
        product_id=1
        qry = "select product_name,stock_quantity,price from product_details where product_id=%s"
        res.execute(qry,(product_id,))
        data=res.fetchall()
        con.commit()
        pro_name=data[0][0]
        stock_quantity=data[0][1]
        price_per_quantity=data[0][2]
        total_amount=quantity*price_per_quantity
        bt=st.button("Submit")

        if bt:
            if quantity<=stock_quantity:
                qry = "insert into order_details (customer_id,product_id,product_name,quantity,price_per_quantity,total_amount) values (%s,%s,%s,%s,%s,%s)"
                val = (customer_id,product_id,pro_name,quantity,price_per_quantity,total_amount)
                res.execute(qry,val)
                con.commit()
                st.info("Order placed ")
            
                #stock_update
            qry = "update product_details set stock_quantity=stock_quantity-%s where product_id=%s"
            val = (quantity,product_id)
            res.execute(qry,val)
            con.commit()
            
        elif quantity>stock_quantity:
            st.info("Product out of Stock")


def cancel_order():
    user_name=st.text_input("User Name",placeholder="Enter the User Name")
    bt=st.button("Submit")
    if bt:
        qry = "select customer_id from customer_details where user_name=%s"
        res.execute(qry,(user_name,))
        dat=res.fetchall()
        con.commit()
        customer_id=dat[0][0]

        qry = "Select order_id,product_name from order_details where customer_id=%s"
        val = (customer_id,)
        res.execute(qry,val)
        data=res.fetchall()
        con.commit()
        order_ids=[]    
        product_names=[]
        for i in data:
            order_ids.append(i[0])
            product_names.append(i[1])
    
        datum={"Order Id":order_ids,"Product Name":product_names}
        st.dataframe(datum)

    order_id=st.text_input("Enter the order ID",placeholder="Enter the Order Id")
    but=st.checkbox("submit")
    if but:
        qry = "select product_id,quantity from order_details where order_id=%s"
        val = (order_id,)
        res.execute(qry,val)
        data = res.fetchall()
        con.commit()
        product_id=data[0][0]
        quantity=data[0][1]
        #updating stock
        qry = "update product_details set stock_quantity = stock_quantity+%s where product_id=%s"
        val =(quantity,product_id)
        res.execute(qry,val)
        con.commit()
        
        #deleting order
        qry = "delete from order_details where order_id=%s"
        val = (order_id,)
        res.execute(qry,val)
        con.commit()
        st.info("Order cancelled")
    
    
def signin():
    customer_id=int(input("Enter your customer id"))
    if customer_id in get_customer_ids():
        ch = input("1.display \n 2.New order \n 3.Cancel order \n 4.Update personal details")
        if ch=="1":
            show_products()
        elif ch=="2":
            show_products()
            new_order()
        elif ch=="3":
            qry = "select order_id,product_name from order_details where customer_id=%s"
            val=(customer_id,)
            res.execute(qry,val)
            data = res.fetchall()
            cancel_order()
        else:
            chk=int(input("1.Name 2.City\n Enter the option you want to update"))
            customer_id=int(input("Enter your customer_id"))
            if chk==1:
                new_name=input("Enter the name you want to change")
                qry = "update customer set customer_name=%s where customer_id=%s"
                val = (new_name,customer_id)
                res.execute(qry,val)
                con.commit()
                print("Name updated Successfully")
            elif chk==2:
                city_name=input("Enter the city name you want to update")
                qry = "update customer set city='%s' where customer_id=%s"
                val = (city_name,customer_id)
                res.execute(qry,val)
                con.commit()
                print("City Name updated Successfully")
            
    else:
        print("Check your customer id")

def order_products():
    qry = "select product_name,price from product_details"
    res.execute(qry)
    data = res.fetchall()
    con.commit()
    product=[]
    price=[]
    for i in data:
        product.append(i[0])
        price.append(i[1])
    
    #datum={"Product Name":product,"Price":price}
    #st.dataframe(datum)
    a=0
    for i in range(0,len(product),3):
        pt1,pt2,pt3=st.columns(3)
        product1=(pt1.subheader(product[a]),pt1.text(price[a]))
        product2=(pt2.subheader(product[a+1]),pt2.text(price[a+1]))
        product3=(pt3.subheader(product[a+2]),pt3.text(price[a+2]))
        a=a+3

#def function_calls():
#   signup()
 #   signin()
  #  new_order()
   # cancel_order()
    #show_products()
    #stock_update()
    #get_customer_ids()
    #get_product_ids()

#function_calls()
def login():    
    user_name=st.text_input("Username",placeholder="Enter Your Username")
    pwsd=st.text_input("Password",placeholder="Enter your password")
    bt=st.button("Submit")

    usernames=[]
    qry = "select user_name from customer_details"
    res.execute(qry)
    data = res.fetchall()
    con.commit()
    for i in data:
        usernames.append(i[0])
    

    if bt:
        if user_name not in usernames:
            st.warning("Invalid Username")
        elif user_name in usernames:
            qry = "select pwd from customer_details where user_name=%s"
            res.execute(qry,(user_name,))
            data = res.fetchall()
            con.commit()
            user_pwd=data[0][0]
            if pwsd!=user_pwd:
                st.error("Incorrect Password")
            else:
                rad = st.radio("Options",["New order","Cancel order"])
                if rad == "Display":
                    show_products()
                
                elif rad == "New order":
                    order_products()
            
                if rad == "Cancel order":
                    qry = "select order_id,product_name from order_details where customer_id=%s"
                    #val=(customer_id,)
                    res.execute(qry,val)
                    data = res.fetchall()
                    cancel_order()
                

st.title("Inventory Management")


rad = st.sidebar.radio("Navigator",["New User? Signup","Signin","Update Personal Details","New Order","Cancel Order","Check"])

if rad == "New User? Signup":
    signup()
  
if rad =="Signin":
    login()
    
if rad == "Update Personal Details":
    radi = st.selectbox("Options",["None","Email","phone"])
    if radi=="Email":
        user_name=st.text_input("Enter your user name")
        new_email=st.text_input("Enter the Email you want to change")
        bt=st.button("Submit")
        if bt:    
            qry = "update customer_details set email=%s where username=%s"
            val = (new_email,user_name)
            res.execute(qry,val)
            con.commit()
            st.info("Email updated Successfully")
    if radi=="phone":
        user_name=st.text_input("Enter your user name")
        city_name=st.text_input("Enter the city name you want to update")
        bt=st.button("Submit")
        if bt:
            qry = "update customer_details set city='%s' where user_name=%s"
            val = (city_name,user_name)
            res.execute(qry,val)
            con.commit()
            print("City Name updated Successfully")

if rad == "New Order":
    new_order()
    
if rad == "Cancel Order":
    cancel_order()




#if rad == "Check":
    #order_products()

