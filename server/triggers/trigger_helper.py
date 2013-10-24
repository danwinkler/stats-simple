import sqlite3
import time
import json

def get_nodes():
	conn = sqlite3.connect( "db.db" )
	conn.row_factory = sqlite3.Row
	db = conn.cursor()
	rows = db.execute('SELECT id,name from nodes').fetchall()
	conn.close()
	nodes = []
	for row in rows:
		nodes.append( { "id": row['id'], "name": row['name'] } )
	return nodes

def latest_node_data( node, name, time_span ):
	conn = sqlite3.connect( "db.db" )
	conn.row_factory = sqlite3.Row
	db = conn.cursor()
	time_ago = time.time() - time_span
	rows = db.execute('SELECT value, time from data where node=? AND name=? AND time >= ?', (node,name,time_ago) ).fetchall()
	conn.close()
	data = []
	for row in rows:
		data.append( { "time": row['time'], "value": json.loads( row['value'] ) } )
	return data

def latest_notes( node, time_span ):
	conn = sqlite3.connect( "db.db" )
	conn.row_factory = sqlite3.Row
	db = conn.cursor()
	time_ago = time.time() - time_span
	rows = db.execute('SELECT note, time from notes where node=? AND time >= ?', (node,name,time_ago) ).fetchall()
	conn.close()
	data = []
	for row in rows:
		data.append( { "time": row['time'], "note": row['note'] } )
	return data

def make_alert( name, value, level ):
	conn = sqlite3.connect( "db.db" )
	db = conn.cursor()
	rows = db.execute('INSERT INTO alerts (name,value,level,time) VALUES (?,?,?,?)', (name,value,level,time.time()) )
	conn.commit()
	conn.close()	