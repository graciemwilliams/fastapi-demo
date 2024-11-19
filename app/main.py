#!/usr/bin/env python3

from fastapi import Request, FastAPI
from typing import Optional
from pydantic import BaseModel
import pandas as pd
import json
import os
import mysql.connector
from mysql.connector import Error

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "tkd5jg"

@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:
        db = mysql.connector.connect(
            host=DBHOST,
            user=DBUSER,
            password=DBPASS,
            database=DB
        )
        cur = db.cursor()    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    finally:
        # Ensure resources are closed properly
        if cur:
            cur.close()
        if db and db.is_connected():
            db.close()

@app.get('/songs')
def get_songs():
    query = "SELECT * FROM songs ORDER BY id;"
    try:    
db = mysql.connector.connect(
            host=DBHOST,
            user=DBUSER,
            password=DBPASS,
            database=DB
        )
        cur = db.cursor()
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    finally:
        # Ensure resources are closed properly
        if cur:
            cur.close()
        if db and db.is_connected():
            db.close()

@app.get("/")  # zone apex
def zone_apex():
    return {"Good Day": "Sunshine!"}

@app.get("/sum/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@app.get("/multiply/{c}/{d}")
def multiply(c: int, d: int):
    return {"product": c * d}

@app.get("/square/{e}")
def square(e: int):
    return {"square": e * e}

@app.get("/data")
def zone_apex():
    return{"This is some data": "Gracie loves apple pie. She also likes pumpkin pie."}

@app.get("/customer/{idx}")
def customer(idx: int):
    # read the data into a df
    df = pd.read_csv("customers.csv")
    # filter the data based on the index
    customer = df.iloc[idx]
    return customer.to_dict()

@app.post("/get_body")
async def get_body(request: Request):
    response = await request.json()
    first_name = response["fname"]
    last_name = response["lname"]
    favorite_number = response["favnu"]
    return {"first_name": first_name, "last_name": last_name, "favorite_number": favorite_number}
