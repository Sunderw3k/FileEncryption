from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
from typing import Optional
import uvicorn
import socket

app = FastAPI()

class Values(BaseModel):
	name: str
	content: str
	hash: str
	key: Optional[str] = None

@app.post("/save")
def database(item: Values):
	if item.key == None:
		return "Key not specified"

	db = sqlite3.connect("database.db")
	cur = db.cursor()
	sql = "INSERT INTO files(name, content, hash, key) VALUES(?,?,?,?)"
	val = (str(item.name), str(item.content), str(item.hash), str(item.key))
	cur.execute(sql,val)
	db.commit()
	return "Success!"

@app.post("/check")
def check(item: Values):
	db = sqlite3.connect("database.db")
	cur = db.cursor()
	cur.execute(f"SELECT hash FROM files WHERE name='{item.name}' AND content='{item.content}'")
	result = cur.fetchone()
	if result is None:
		return 404
	if result[0] == item.hash:
		cur.execute(f"SELECT key FROM files WHERE name='{item.name}' AND content='{item.content}'")
		result = cur.fetchone()
		return result[0]
	else:
		return 403

if __name__ == "__main__":
	hostname = socket.gethostname()
	ip = socket.gethostbyname(hostname)
	print(ip)
	uvicorn.run("server:app", host=ip, reload=True)
