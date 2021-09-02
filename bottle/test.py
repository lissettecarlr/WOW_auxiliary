
from bottle import route ,run

@route('/message')
def hello():
    return "1111111111"

run(host='localhost',port=2333,debuf=True)
