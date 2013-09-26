from bottle import route, run, template
from bottle.ext import sqlite
import bottle

app = bottle.Bottle()
plugin = sqlite.Plugin(dbfile='/db.db')
app.install(plugin)

@app.post('/data')
def data(db):
    return "hello"

run(host='localhost', port=8080)