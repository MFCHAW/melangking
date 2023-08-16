import streamlit as st
import pymssql

conn = pymssql.connect(server='quarto-vm2.southeastasia.cloudapp.azure.com', port='14336', user='quartobi', password='Rohs85#', database='LONE_PTWP')
cursor = conn.cursor(as_dict=True)

cursor.execute('Select * from GMS_UOMStp')
for row in cursor:
  print (row)
  
# for row in cursor:
#     print("ID=%d, Name=%s" % (row['id'], row['name']))

conn.close()