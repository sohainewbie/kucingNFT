from app import app
import mysql.connector

def connect():
    con = mysql.connector.connect(**app.config['config']["db"])
    return con