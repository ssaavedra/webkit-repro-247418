import uuid
from bottle import HTTPError, redirect, request, route, run, template
from bottle_sqlite import SQLitePlugin
import sqlite3

sqlite_plugin = SQLitePlugin(dbfile='./db.sqlite3')


@route('/')
def index():
    return template('front.html')

@route('/login', apply=[sqlite_plugin], method=["GET", "POST"])
def login_action(db: sqlite3.Connection):
    # Create token
    id = uuid.uuid4().hex
    db.execute("INSERT INTO login_tokens (hash) VALUES (?)", [id])
    return {"token": id}


@route('/logout/<token>', apply=[sqlite_plugin])
def logout_action(token: str, db: sqlite3.Connection):
    # Check token
    count = db.execute("DELETE FROM login_tokens WHERE hash = ?", [token]).rowcount
    return {"status": "ok", "msg": "Deleted {} rows".format(count)}

@route('/perform', apply=[sqlite_plugin])
def perform_redir():
    return redirect("/perform/", code=301)  # Code 301 is relevant for this bug. Code 303 See Other will not exhibit the buggy behavior.

@route('/perform/', apply=[sqlite_plugin])
def perform_action(db: sqlite3.Connection):
    # Check token
    try:
        auth: str = request.get_header('authorization')
        token = auth.split(" ")[1]
        count = list(db.execute("SELECT COUNT(*) FROM login_tokens WHERE hash = ?", [token]).fetchone())[0]
        print("What count is: ", count)
        if count > 0:
            return {"status": "ok", "token": token, "count": count}
        raise HTTPError(status=401, body=f'{{"msg": "unauthorized for token {token}"}}')

    except HTTPError:
        raise
    except Exception as e:
        print("Got exception: ", e)
        raise HTTPError(status=401, body=f'{{"error": "{e}", "msg": "unauthorized for token {token}"}}', exception=e)


if __name__ == '__main__':
    db = sqlite3.connect('./db.sqlite3')
    db.execute("CREATE TABLE IF NOT EXISTS login_tokens (id INTEGER PRIMARY KEY AUTOINCREMENT, hash VARCHAR(128) NOT NULL);")
run(host='0.0.0.0', port=8080)
