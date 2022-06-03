import random, json
import mysql.connector
from app.utils.db import *


def generateCat():
    colors = ['brownblack', 'brown', 'white', 'whiteblack', 'graywhite']
    images = {
        'brown' : 'http://68.183.190.243:8083/images/001.jpeg',
        'white'  : 'http://68.183.190.243:8083/images/002.jpeg',
        'graywhite'  : 'http://68.183.190.243:8083/images/003.jpeg',
        'brownblack'  : 'http://68.183.190.243:8083/images/004.jpeg',
        'whiteblack'  : 'http://68.183.190.243:8083/images/005.jpeg',
    }
    skills = [ ['meditation', 'focus'],
        ['smart', 'lazy'],
        ['dummy', 'joyful'],
         ['guru', 'diligent'],
        ['wisdom' , 'support']]
    
    color = random.choice(colors)
    image = images[color]
    skill =  random.choice(skills)
    rarity = random.choice([1,2,3,4,5])
    level = 0
    data = {
			"color" : color,
			"image" : image,
			"rarity" : rarity,
			"level" : level,
			"skills" : json.dumps(skill)
		}
    return data

def getCats(tokenId):
    con = connect()
    
    queryCats = "SELECT * FROM cats where tokenId={}".format(tokenId)
    print(queryCats)
    
    cursor = con.cursor()
    cursor.execute(queryCats)
    data = cursor.fetchone()
    con.close()
    
    return data

def minting(payload):
    error = ""
    con = connect()
    
    address = payload['address']
    tokenId = payload['tokenId']
    color = payload['color']
    image = payload['image']
    rarity = payload['rarity']
    level = payload['level']
    skills = payload['skills']

    insertCat = "INSERT INTO cats SET address='{}', tokenId={}, color='{}', image='{}', rarity={}, level={}, skills='{}', created_at=now();".format(
        address, tokenId, color, image, rarity, level, skills
    )
    print(insertCat)
    
    cursor = con.cursor()
    cursor.execute(insertCat)
    con.commit()
    con.close()
    
    return error