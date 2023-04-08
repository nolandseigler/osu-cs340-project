import os
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import Connection
from sqlalchemy.sql import text

from what_the_fec.storage.db import init as db_init
from what_the_fec.storage.mysql.config import MySQLConfig

# this doesnt feel great but works for today
from what_the_fec.storage.mysql.db import get_db


def create_app() -> FastAPI:
    app = FastAPI()
    db_init(config=MySQLConfig(
            db_user=os.environ["MARIA_DB_USER"],
            db_password=os.environ["MARIA_DB_PASSWORD"],
            db_hostname=os.environ["MARIA_DB_HOSTNAME"],
            db_port=os.environ["MARIA_DB_PORT"],
            db_name=os.environ["MARIA_DB_NAME"],
            pool_connections=2
        )
    )
    db = get_db()

    # Citation for the following code:
    # Date: 04/06/2023
    # Copied from /OR/ Adapted from /OR/ Based on:
    # FastAPI/SQLAlchemy documentation examples
    @app.get("/assignment_1")
    def assignment_1(conn: Connection = Depends(db.get_conn)):
        
        sql = """
            DROP TABLE IF EXISTS diagnostic;
        """
        conn.execute(text(sql))

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
