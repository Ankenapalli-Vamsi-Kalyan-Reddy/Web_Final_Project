from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

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

class Item(BaseModel):
    id: int 
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    try:
        curr.execute("INSERT OR IGNORE INTO items (id, name, price) VALUES (?, ?, ?);", (item.id, item.name, item.price))
        if curr.rowcount > 0:
            conn.commit()
            return Item(id=item.id, name=item.name, price=item.price)
        else:
            return {"message": "Item with that ID already exists"}

    finally:
        conn.close()



@app.get("/items/{item_id}")
def read_item(item_id: int):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("SELECT id, name, price FROM items WHERE id = ?", (item_id,))
    item = curr.fetchone()
    conn.close()

    if item is not None:
        return {"id": item[0], "name": item[1], "price": item[2]}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
   
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item.id != item_id:
        raise HTTPException(status_code=400, detail="Item ID does not match ID in path")
    
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    try:
        curr.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        existing_item = curr.fetchone()
        if existing_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        curr.execute("UPDATE items SET name=?, price=? WHERE id=?;", (item.name, item.price, item_id))
        conn.commit()
        return {"message": "Item updated successfully"}
    finally:
        conn.close()

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("DELETE FROM items WHERE id=?;", (item_id,))
    total_changes = conn.total_changes
    conn.commit()
    conn.close()
    if total_changes != 1:
        raise HTTPException(status_code=400, detail=f"{total_changes} rows affected")
    return total_changes

