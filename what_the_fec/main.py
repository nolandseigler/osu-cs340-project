import os

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from what_the_fec.dependencies import get_db_conn, get_templates, templates_init
from what_the_fec.routes.candidate_office_records.routes import (
    router as candidate_office_records_router,
)
from what_the_fec.routes.candidates.routes import router as candidates_router
from what_the_fec.routes.committees.routes import router as committees_router
from what_the_fec.routes.contributions.routes import router as contributions_router
from what_the_fec.routes.election_years.routes import router as election_years_router
from what_the_fec.routes.home.routes import router as home_router
from what_the_fec.storage.db import init as db_init
from what_the_fec.storage.mysql.config import MySQLConfig


def create_app() -> FastAPI:
    templates_init(
        templates=Jinja2Templates(directory=os.environ["TEMPLATES_DIR_PATH"])
    )

    db_init(
        config=MySQLConfig(
            db_user=os.environ["MARIA_DB_USER"],
            db_password=os.environ["MARIA_DB_PASSWORD"],
            db_hostname=os.environ["MARIA_DB_HOSTNAME"],
            db_port=os.environ["MARIA_DB_PORT"],
            db_name=os.environ["MARIA_DB_NAME"],
            pool_connections=2,
        )
    )

    app = FastAPI(
        dependencies=[Depends(get_db_conn), Depends(get_templates)],
    )
    app.mount(
        "/static", StaticFiles(directory=os.environ["STATIC_DIR_PATH"]), name="static"
    )

    app.include_router(home_router)

    app.include_router(candidates_router)
    app.include_router(candidate_office_records_router)
    app.include_router(committees_router)
    app.include_router(contributions_router)
    app.include_router(election_years_router)

    return app
