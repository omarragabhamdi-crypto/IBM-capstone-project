#!/bin/bash

# أمر لتصدير بيانات جدول sales_data إلى ملف sales_data.sql
mysqldump --host=172.21.20.104 --port=3306 --user=root --password=luxFlyAFINi1srGSA01cSOqd sales sales_data > sales_data.sql

echo "Data export completed successfully to sales_data.sql!"
