import streamlit as st
import mysql.connector

con = mysql.connector.connect(host="localhost",user="root",password="12345",database="inventory_management")
res = con.cursor()

st.title("Inventory Management Admin")

rad = st.sidebar.radio("Navigator",["Employee Sign Up","Employee Sign in ","Stock Update","New Stock","Remove Products","Employee Details","User Info"])

if rad == "Employee Sign Up":
    emp_name=st.text_input("Name",placeholder="Enter your name")
    
    mail,ph=st.columns([2,1])
    email=mail.text_input("Email",placeholder="Enter your Email")
    mobile_no=ph.text_input("Phone number",placeholder="Enter your Phone number")
    mobile_no=int()
    emp_user_name=st.text_input("Employee Username",placeholder="choose your user name")
    
    pwsd,pwsd1=st.columns(2)
    
    pwd=pwsd.text_input("Password",placeholder="Choose your password")
    re_password=pwsd1.text_input("Re-Password",placeholder="Re-Enter the password")
    
    bt=st.button("Submit")

    usernames=[]
    qry = "select emp_user_name from employee_details"
    res.execute(qry) 
    data = res.fetchall()
    con.commit()
    for i in data:
        usernames.append(i[0])
    
    if bt:
        if emp_user_name in usernames:
            st.warning("Employee User name already exist")
        elif pwd!=re_password:
            st.warning("Password mismatch")
        else:
            st.info("successfull")
            qry = "insert into employee_details (emp_name,email,mobile_no,emp_user_name,pwd) values (%s,%s,%s,%s,%s)"
            val = (emp_name,email,mobile_no,emp_user_name,pwd)
            res.execute(qry,val)
            con.commit()

if rad == "Employee Sign in ":
    emp_user_name=st.text_input("Username",placeholder="Enter Employee Your Username")
    pwsd=st.text_input("Password",placeholder="Enter your password")
    bt=st.button("Submit")

    usernames=[]
    qry = "select emp_user_name from employee_details"
    res.execute(qry)
    data = res.fetchall()
    con.commit()
    for i in data:
        usernames.append(i[0])
    

    if bt:
        if emp_user_name not in usernames:
            st.warning("Invalid Username")
        elif emp_user_name in usernames:
            qry = "select pwd from employee_details where emp_user_name=%s"
            res.execute(qry,(emp_user_name,))
            data = res.fetchall()
            con.commit()
            user_pwd=data[0][0]
            if pwsd!=user_pwd:
                st.warning("Invalid Password")
            else:
                st.info("Successfull")
  
if rad == "Stock Update":
    qry = "select product_id,product_name,stock_quantity from product_details"
    res.execute(qry)
    data = res.fetchall()
    con.commit()
    product=[]
    stock_quantity=[]
    product_id=[]
    for i in data:
        product_id.append(i[0])
        product.append(i[1])
        stock_quantity.append(i[2])
    
    datum={"Product Id":product_id,"Product Name":product,"Stock Quantity":stock_quantity}
    st.dataframe(datum)

    pro_id,quan=st.columns(2)
    productid=pro_id.text_input("Product Id",placeholder="Enter the product id")
    quantity=quan.text_input("Update Quantity",placeholder="Enter the quantity to add")
    bt=st.button("Submit")
    if bt:
        qry = "update product_details set stock_quantity=stock_quantity+%s where product_id=%s"
        val = (quantity,productid)
        res.execute(qry,val)
        con.commit()
        st.info("Successful")

if rad == "New Stock":
    product_name=st.text_input("Product Name",placeholder="Enter the Product Name")
    stock_quantity=st.number_input("Quantity",placeholder="Enter the Quantity",min_value=0,value=0,step=1)
    price=st.text_input("Price",placeholder="Enter the Price")    
    price=int()
    bt=st.button("Submit")

    if bt:
        qry = "insert into product_details (product_name,stock_quantity,price) values (%s,%s,%s)"
        val = (product_name,stock_quantity,price)
        res.execute(qry,val)
        con.commit()

if rad == "Remove Products":
    qry = "select product_id,product_name,stock_quantity from product_details"
    res.execute(qry)
    data = res.fetchall()
    con.commit()
    product=[]
    stock_quantity=[]
    product_id=[]
    for i in data:
        product_id.append(i[0])
        product.append(i[1])
        stock_quantity.append(i[2])
    
    datum={"Product Id":product_id,"Product Name":product,"Stock Quantity":stock_quantity}
    st.dataframe(datum)
    
    pro_id=st.text_input("Product Id",placeholder="Enter the Product Id")
    bt=st.button("Submit")
    
    if bt:
        qry = "delete from product_details where product_id=%s"
        res.execute(qry,(pro_id,))
        con.commit()


if rad == "Employee Details":
    qry = "select emp_id,emp_name,emp_user_name,mobile_no from employee_details"
    res.execute(qry)
    data = res.fetchall()
    con.commit()
    emp_ids=[]
    emp_names=[]
    emp_user_names=[]
    mobile_nos=[]
    for i in data:
        emp_ids.append(i[0])
        emp_names.append(i[1])
        emp_user_names.append(i[2])
        mobile_nos.append(i[3])
    
    datum={"Employee Id":emp_ids,"Employee Name":emp_names,"Employee User Name":emp_user_names,"Mobile No":mobile_nos}
    st.dataframe(datum)

if rad == "User Info":
    qry = "select customer_id,user_name,phone from customer_details"
    res.execute(qry)
    data = res.fetchall()
    con.commit()
    cus_ids=[]
    user_names=[]
    mobile_nos=[]
    for i in data:
        cus_ids.append(i[0])
        user_names.append(i[1])
        mobile_nos.append(i[2])
    
    datum={"Customer Id":cus_ids,"User Name":user_names,"Mobile No":mobile_nos}
    st.dataframe(datum)

