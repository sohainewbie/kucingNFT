import mysql.connector
from app.utils.db import *


def getTrx(payload):
    error = ""
    
    con = connect()
    payloadStr = "{}".format(payload)
    address = payload['address']
    block_hash = payload['transaction']

    searchTransactions = "SELECT * FROM transactions where block_hash='{}'".format(block_hash)
    insertTransactions = "INSERT INTO transactions SET address='{}', block_hash='{}', created_at=now();".format(address, block_hash)

    cursor = con.cursor()
    cursor.execute(searchTransactions)
    print(searchTransactions)

    data = cursor.fetchone()
    if data == None:
        cursor.execute(insertTransactions)
        con.commit()
    else:
        error = "Transaction Already Exist"
    con.close()
    
    return error