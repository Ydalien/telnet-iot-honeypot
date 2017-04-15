import hashlib

from db import get_db

from util.dbg import dbg

# Controls Actions perfomed by Honeypot Clients
class ClientController:
	
	def __init__(self):
		pass
		
	def put_session(self, session):
		db = get_db()
		
		try:
			s_id = db.put_conn(session["ip"], session["user"], session["pass"], session["date"])
			req_urls = []
			
			for url in session["urls"]:
				db_url = db.get_url(url).fetchone()
				url_id = 0
				
				if db_url == None:
					url_id = db.put_url(url, session["date"])
					req_urls.append(url)
					
				elif db_url["sample"] == None:
					req_urls.append(url)
					url_id = db_url["id"]
					
				else:
					# Sample exists already
					# TODO: Check url for oldness
					pass
					
				db.link_conn_url(s_id, url_id)
			
			return req_urls
		
		finally:
			db.end()
	
	def put_sample_info(self, f):
		db = get_db()
		
		try:
			url = f["url"]
			url_id = db.get_url(url).fetchone()["id"]
			
			sample_id = db.put_sample(f["sha256"], f["name"], f["length"], f["date"])
			db.link_url_sample(url_id, sample_id)
			return f
	
		finally:
			db.end()
	
	def put_sample(self, data):
		db = get_db()
		
		try:
			sha256 = hashlib.sha256(data).hexdigest()
			db.put_sample_data(sha256, data)
		
		finally:
			db.end()