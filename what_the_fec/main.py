from fastapi import Depends, FastAPI
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

        sql = """
            CREATE TABLE diagnostic(id INT PRIMARY KEY, text VARCHAR(255) NOT NULL);
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
        result = conn.execute(text(sql), *bind_params)
        print(result.all()[0])

        return {"Hello": "World"}

    return app
