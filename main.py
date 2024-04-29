from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

'''customers = [
    (0, "609-555-0124", "Karl"),
    (1, "609-555-1234", "Mike"),
    (3, "609-555-4302", "Ryan"),
]

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    for cust_id, phone, name in customers:
        if cust_id == customer_id:
            return {"customer_id": cust_id, "phone": phone, "name": name}
    return {"error": "Customer not found"}
'''

class Customer(BaseModel):
    cust_id: int | None = None
    name: str
    phone: str

@app.post("/customers/")
def create_item(customer: Customer):
    if customer.cust_id != None:
        raise HTTPException(status_code=400, detail="cust_id cannot be set on POST request")
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (customer.name, customer.phone))
    customer.cust_id = curr.lastrowid
    conn.commit()
    conn.close()
    return customer

@app.get("/customers/{cust_id}")
def read_item(cust_id: int, q=None):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("SELECT id, name, phone FROM customers WHERE id=?", (cust_id,))
    customer = curr.fetchone()
    conn.close()
    if customer != None:
        return Customer(cust_id=customer[0], name=customer[1], phone=customer[2])
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
@app.put("/customers/{cust_id}")
def update_customer(cust_id: int, customer: Customer):
    if customer.cust_id != None and customer.cust_id != cust_id:
        raise HTTPException(status_code=400, detail="Customer ID does not match ID in path")
    customer.cust_id = cust_id
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("UPDATE customers SET name=?, phone=? WHERE id=?;", (customer.name, customer.phone, cust_id))
    total_changes = conn.total_changes
    conn.commit()
    conn.close()
    if total_changes == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return customer

@app.delete("/customers/{cust_id}")
def delete_customer(cust_id: int):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("DELETE FROM customers WHERE id=?;", (cust_id,))
    total_changes = conn.total_changes
    conn.commit()
    conn.close()
    if total_changes != 1:
        raise HTTPException(status_code=400, detail=f"{total_changes} rows affected")
    return total_changes