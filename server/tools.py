import argparse
import sqlite3
import sys
from argparse import RawTextHelpFormatter

def rm_node( node ):
	conn = sqlite3.connect( "db.db" )
	conn.row_factory = sqlite3.Row
	db = conn.cursor()
	
	print "Finding node..."
	node_row = db.execute('SELECT id from nodes where name=?', (node,)).fetchone()
	if node_row == None:
		print "No row with name: " + node
		sys.exit()

	node_id = int(node_row['id'])

	print "Deleting data..."
	rows = db.execute('DELETE FROM data WHERE node=?', (node_id,) )
	conn.commit()
	print "Deleting notes..."
	rows = db.execute('DELETE FROM notes WHERE node=?', (node_id,) )
	conn.commit()
	print "Deleting node..."
	rows = db.execute('DELETE FROM nodes WHERE id=?', (node_id,) )
	conn.commit()
	conn.close()
	print "Done!"

def no_command( args ):
	print "Bad Command: " + str(args.command)

def create_db( args=None ):
	con = sqlite3.connect( 'db.db' )
	con.execute( """CREATE TABLE alerts (
		id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
		name VARCHAR(60) NOT NULL, 
		value TEXT NOT NULL, 
		level INTEGER NOT NULL, 
		time INTEGER NOT NULL, 
		sentmail INTEGER NOT NULL)"""
	)

	con.execute( """CREATE TABLE data (
		id INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
		node INTEGER NOT NULL,
		name VARCHAR(60) NOT NULL,
		type VARCHAR(60) NOT NULL,
		value TEXT NOT NULL,
		time INTEGER NOT NULL)""" 
	)

	con.execute( """CREATE TABLE nodes (
		id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		name VARCHAR(60) NOT NULL,
		node_group VARCHAR(60) NOT NULL,
		collectors TEXT NOT NULL,
		annotators TEXT NOT NULL)"""
	)

	con.execute( """CREATE TABLE notes (
		id INTEGER,
		node VARCHAR(60),
		note TEXT,
		time INTEGER)""" 
	)

	con.execute( "CREATE INDEX data_index ON data (node,name,time)" )
	con.execute( "CREATE INDEX alerts_index ON alerts (time)" )
	con.execute( "CREATE INDEX notes_index ON notes (node,time)" )

	con.commit()
	con.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser( formatter_class=RawTextHelpFormatter, description='''
	Stats-Simple Command Line Tool
	Available commands:
	rm-node
	''' )

	parser.add_argument("command", help="The command you want to run")
	parser.add_argument("arg")

	args = parser.parse_args()

	{ "rm-node": rm_node, "create-db": create_db }.get( args.command, no_command )( args.arg )