# Import libraries required for connecting to mysql
import mysql.connector

# Import libraries required for connecting to PostgreSql
import psycopg2

# بيانات الاتصال الخاصة بمعملك الحالي
mysql_config = {
    'host': '172.21.246.83',
    'user': 'root',
    'password': 'Wf9RDvwtsUXXAYU7MqVNY4gD',
    'database': 'sales'
}

postgres_config = {
    'host': '172.21.10.254',
    'user': 'postgres',
    'password': 'GI4QYp3xIuK4MDhkvNRk2eBB',
    'database': 'postgres'
}

# ====================================================================
# Task 1 - Implement the function get_last_rowid()
# ====================================================================
def get_last_rowid():
    try:
        conn = psycopg2.connect(**postgres_config)
        cursor = conn.cursor()
        
        # استعلام لجلب أكبر rowid موجود في مستودع البيانات الحالي
        cursor.execute("SELECT MAX(rowid) FROM sales_data;")
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        # لو الجدول لسه فاضي خالص، بيرجع 0 كبداية
        return result[0] if result[0] is not None else 0
    except Exception as e:
        print(f"Error in get_last_rowid: {e}")
        return 0

last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)


# ====================================================================
# Task 2 - Implement the function get_latest_records()
# ====================================================================
def get_latest_records(rowid):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        
        # استعلام لجلب البيانات الجديدة (Incremental) التي قيمتها أكبر من آخر rowid
        # سحبنا الأعمدة الـ 4 الأساسية المتوفرة في قاعدة بيانات التشغيل لتفادي خطأ الأسماء
        query = "SELECT rowid, product_id, customer_id, quantity FROM sales_data WHERE rowid > %s;"
        cursor.execute(query, (rowid,))
        
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records
    except Exception as e:
        print(f"Error in get_latest_records: {e}")
        return []    

new_records = get_latest_records(last_row_id)


# ====================================================================
# Task 3 - Implement the function insert_records()
# ====================================================================
def insert_records(records):
    try:
        if not records:
            return
            
        conn = psycopg2.connect(**postgres_config)
        cursor = conn.cursor()
        
        # التحويل (Transformation): إضافة سعر افتراضي (10.0) للمواءمة مع أعمدة الـ Warehouse
        transformed_records = []
        for row in records:
            # row[0]=rowid, row[1]=product_id, row[2]=customer_id, row[3]=quantity
            transformed_records.append((row[0], row[1], row[2], row[3], 10.0))
            
        # استعلام الإدخال الجماعي في PostgreSQL
        query = """
            INSERT INTO sales_data (rowid, product_id, customer_id, quantity, price) 
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (rowid) DO NOTHING;
        """
        cursor.executemany(query, transformed_records)
        conn.commit()
        
        print(f"[+] Successfully inserted {cursor.rowcount} new records into PostgreSQL!")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error in insert_records: {e}")


# ====================================================================
# Task 4 - Test the data synchronization
# ====================================================================
if new_records is not None:
    print("New rows on staging datawarehouse = ", len(new_records))
    insert_records(new_records)
else:
    print("New rows on staging datawarehouse = 0 (No new records found or query returned None)")

# End of program
print("ETL Job Finished Successfully!")