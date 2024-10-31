from sqlalchemy import create_engine, insert, text, Table, MetaData

class Storage:
    
    url = "mysql+mysqlconnector://{USER}:{PWD}@{HOST}/{DBNAME}"
    url = url.format(USER = "root", PWD = "Farida1?", HOST = "localhost:3306", DBNAME = "crm_db")

    def __init__(self):
        pass
        
    
    def connect_db(self):
        return create_engine(self.url)
    

    def read_table(self, obj_name):
        if (obj_name=='Customer'):
            read_query = text("SELECT * FROM crm_db.customer_info ORDER BY cust_id DESC;")
        elif (obj_name=='Product'):
            read_query = text("SELECT * FROM crm_db.product_info ORDER BY product_id DESC;")
        elif (obj_name=='Staff'):
            read_query = text("SELECT * FROM crm_db.staff_info ORDER BY staff_id DESC;")
        elif (obj_name=='Sales'):
            read_query = text("SELECT * FROM order_log ORDER BY log_id DESC;")
        elif (obj_name=='Sales_Order'):
            read_query= text("SELECT * FROM order_info;")
        engine = self.connect_db()
        with engine.connect() as conn:
            result = conn.execute(read_query).fetchall()
        return(result)
    

    def search(self, obj_name, keyword):
        if (obj_name=='Customer' or obj_name=='Order_customer'):
            search_query = text("SELECT * FROM crm_db.customer_info WHERE (INSTR(cust_name,'{}') != 0) ORDER BY cust_id DESC;".format(keyword))
        elif (obj_name=='Product' or obj_name=='Order_product'):
            search_query = text("SELECT * FROM crm_db.product_info WHERE (INSTR(product_name,'{}') != 0) ORDER BY product_id DESC;".format(keyword))
        elif (obj_name=='Staff' or obj_name=='Order_rep'):
            search_query = text("SELECT * FROM crm_db.staff_info WHERE (INSTR(staff_name,'{}') != 0) ORDER BY staff_id DESC;".format(keyword))
        elif (obj_name == 'Sales'):
            search_query= text("SELECT * FROM order_log WHERE (INSTR(cust_name,'{}') != 0) ORDER BY log_id DESC;".format(keyword))
        elif (obj_name == 'Sales_Order'):
            search_query= text("SELECT * FROM order_log WHERE log_id = {};".format(keyword))
        
        engine = self.connect_db()
        with engine.connect() as conn:
            result = conn.execute(search_query).fetchall()
        return(result)


    def delete(self, obj_name, id):
        if (obj_name=='Customer'):
            del_query = text("DELETE FROM customer_info WHERE cust_id ={};".format(id))
        elif (obj_name=='Product'):
            del_query = text("DELETE FROM product_info WHERE product_id ={};".format(id))
        elif (obj_name=='Staff'):
            del_query = text("DELETE FROM staff_info WHERE staff_id ={};".format(id))
        elif (obj_name=='Sales'):
            del_query= text("DELETE FROM order_info WHERE order_id = {};".format(id))
            query = text("DELETE FROM order_log WHERE log_id = {};".format(id))
        elif (obj_name == 'Sales_Order'):
            del_query= text("DELETE FROM order_info WHERE line_id = {};".format(id))
        engine = self.connect_db()
        with engine.connect() as conn:
                conn.execute(del_query)
                conn.commit()
                if (obj_name == 'Sales'):
                    conn.execute(query)
                    conn.commit()


    def update(self, obj_name, my_args, id):
        if (obj_name=='Customer'):
            update_query= text("UPDATE customer_info SET cust_name='{}', cust_email='{}', cust_phone_num = '{}', cust_address= '{}' WHERE cust_id={};".format(my_args[0], my_args[1], my_args[2], my_args[3], id))
        elif (obj_name=='Product'):
            update_query= text("UPDATE product_info SET product_name='{}', product_description='{}', price = {} WHERE product_id={};".format(my_args[0], my_args[1], my_args[2], id))
        elif (obj_name=='Staff'):
            update_query= text("UPDATE staff_info SET staff_name='{}', staff_email='{}', staff_phone_num = '{}', staff_position = '{}', department = '{}' WHERE staff_id={};".format(my_args[0], my_args[1], my_args[2], my_args[3], my_args[4], id))
        elif (obj_name== 'Order_log'):
            update_query= text("UPDATE order_log SET cust_name='{}', total_amount={}, sales_rep='{}', order_date = '{}' WHERE log_id={};".format(my_args[0], my_args[1], my_args[2], my_args[3], id))
        elif (obj_name == 'Order_info'):
            update_query= text("UPDATE order_info SET product_name='{}', price={}, quantity={} WHERE line_id={};".format(my_args[0], my_args[1], my_args[2], id))
        engine = self.connect_db()
        with engine.connect() as conn:
            conn.execute(update_query)
            conn.commit()

    
    def create(self, obj_name, my_args):      
        if (obj_name=='Customer'):
            create_query= text("INSERT INTO customer_info (cust_name, cust_email, cust_phone_num, cust_address) VALUES ('{}', '{}', '{}', '{}')".format(my_args[0], my_args[1], my_args[2], my_args[3]))
        if (obj_name=='Product'):
            create_query= text("INSERT INTO product_info (product_name, product_description, price) VALUES ('{}', '{}', {})".format(my_args[0], my_args[1], my_args[2]))    
        if (obj_name=='Staff'):
            create_query= text("INSERT INTO staff_info (staff_name, staff_email, staff_phone_num, staff_position, department) VALUES ('{}', '{}', '{}', '{}', '{}')".format(my_args[0], my_args[1], my_args[2], my_args[3], my_args[4]))
        if (obj_name=='Sales'):
            create_query= text("INSERT INTO order_log (cust_name, total_amount, sales_rep, order_date) VALUES ('{}', {}, '{}', '{}')".format(my_args[0], my_args[1], my_args[2], my_args[3]))    
        if (obj_name=='Orders'):
            create_query= text("INSERT INTO order_info (order_id, product_name, price, quantity) VALUES ({}, '{}', {}, {})".format(my_args[0], my_args[1], my_args[2], my_args[3]))    
        engine = self.connect_db()
        with engine.connect() as conn:
            conn.execute(create_query)
            conn.commit()
            id = conn.execute(text("SELECT last_insert_id();")).fetchall()
        if (obj_name=='Sales'):
            return id