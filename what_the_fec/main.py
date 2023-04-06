from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import Connection
from sqlalchemy.sql import text

from what_the_fec.storage.db import init as db_init
from what_the_fec.storage.sqlite.config import SqliteConfig

# this doesnt feel great but works for today
from what_the_fec.storage.sqlite.db import get_db


def create_app() -> FastAPI:
    app = FastAPI()
    db_init(config=SqliteConfig(pool_connections=2))
    db = get_db()
    @app.get("/assignment_1")
    def assignment_1(conn: Connection = Depends(db.get_conn)):
        
        sql = """
            DROP TABLE IF EXISTS diagnostic;
        """
        conn.execute(text(sql))

        # this also gross but since we are playing the raw sql game we get to play the
        # dialect game too. yayyyyy
        if conn.engine.dialect.name == "sqlite":
            id_col = "id INTEGER PRIMARY KEY AUTOINCREMENT"
        else:
            id_col = "id INT PRIMARY KEY AUTO_INCREMENT"
        sql = f"""
            CREATE TABLE diagnostic({id_col}, text VARCHAR(255) NOT NULL);
        """
        conn.execute(text(sql))

        sql = """
            INSERT INTO diagnostic (text) VALUES (:text);
        """
        bind_params = [
            {"text": "MySQL is working"},
        ]
        conn.execute(text(sql), *bind_params)
        conn.commit()

        sql = """
            SELECT * FROM diagnostic;
        """
        output = [{"id": r[0], "text": r[1]} for r in conn.execute(text(sql), *bind_params)]

        return HTMLResponse(f"<h1>MySQL Results {output}<h1/>", 200)

    return app
