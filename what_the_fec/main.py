import os
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection
from sqlalchemy.sql import text
from what_the_fec.api.candidate_office_records import get_all_candidate_office_records_func

from what_the_fec.storage.db import init as db_init
from what_the_fec.storage.mysql.config import MySQLConfig

# this doesnt feel great but works for today
from what_the_fec.storage.mysql.db import get_db


def create_app() -> FastAPI:
    app = FastAPI()
    app.mount("/static", StaticFiles(directory=os.environ["STATIC_DIR_PATH"]), name="static")
    templates = Jinja2Templates(directory=os.environ["TEMPLATES_DIR_PATH"])

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


    @app.get("/candidate_office_records", response_class=HTMLResponse)
    def get_all_candidate_office_records(request: Request,  conn: Connection = Depends(db.get_conn)):
        return get_all_candidate_office_records_func(conn=conn, request=request, templates=templates)

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

        return HTMLResponse(
            f"""
            <h1>
            MySQL Results:
            <h1/>
            {output}
            """, 200
        )

    return app
