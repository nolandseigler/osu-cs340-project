import os

import structlog
from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from what_the_fec.dependencies import get_db_conn, get_templates, templates_init
from what_the_fec.logging import logging_init
from what_the_fec.routes.amendment_indicators.routes import (
    router as amendment_indicators_router,
)
from what_the_fec.routes.candidate_office_records.routes import (
    router as candidate_office_records_router,
)
from what_the_fec.routes.candidate_office_records_committees.routes import (
    router as candidate_office_records_committees_router,
)
from what_the_fec.routes.candidate_office_records_contributions.routes import (
    router as candidate_office_records_contributions_router,
)
from what_the_fec.routes.candidates.routes import router as candidates_router
from what_the_fec.routes.committee_types.routes import router as committee_types_router
from what_the_fec.routes.committees.routes import router as committees_router
from what_the_fec.routes.contributions.routes import router as contributions_router
from what_the_fec.routes.contributor_types.routes import (
    router as contributor_types_router,
)
from what_the_fec.routes.cycles.routes import router as cycles_router
from what_the_fec.routes.cycles_candidate_office_records.routes import (
    router as cycles_candidate_office_records_router,
)
from what_the_fec.routes.cycles_contributions.routes import (
    router as cycles_contributions_router,
)
from what_the_fec.routes.election_years.routes import router as election_years_router
from what_the_fec.routes.election_years_candidate_office_records.routes import (
    router as election_years_candidate_office_records_router,
)
from what_the_fec.routes.election_years_contributions.routes import (
    router as election_years_contributions_router,
)
from what_the_fec.routes.home.routes import router as home_router
from what_the_fec.routes.incumbent_challenger_statuses.routes import (
    router as incumbent_challenger_statuses_router,
)
from what_the_fec.routes.office_types.routes import router as office_types_router
from what_the_fec.routes.party_types.routes import router as party_types_router
from what_the_fec.routes.report_types.routes import router as report_types_router
from what_the_fec.routes.transaction_types.routes import (
    router as transaction_types_router,
)
from what_the_fec.storage.db import init as db_init
from what_the_fec.storage.mysql.config import MySQLConfig

logging_init(log_level="DEBUG")
logger = structlog.get_logger(__name__)


def create_app() -> FastAPI:
    logger.info("begin application creation")
    templates_init(
        templates=Jinja2Templates(directory=os.environ["TEMPLATES_DIR_PATH"])
    )

    logger.debug("initializing db")
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
    logger.debug("mounting static")
    app.mount(
        "/static", StaticFiles(directory=os.environ["STATIC_DIR_PATH"]), name="static"
    )

    logger.debug("including routers")
    app.include_router(home_router)

    app.include_router(amendment_indicators_router)
    app.include_router(candidates_router)
    app.include_router(candidate_office_records_router)
    app.include_router(candidate_office_records_committees_router)
    app.include_router(candidate_office_records_contributions_router)
    app.include_router(committees_router)
    app.include_router(committee_types_router)
    app.include_router(contributions_router)
    app.include_router(contributor_types_router)
    app.include_router(cycles_router)
    app.include_router(cycles_candidate_office_records_router)
    app.include_router(cycles_contributions_router)
    app.include_router(election_years_router)
    app.include_router(election_years_candidate_office_records_router)
    app.include_router(election_years_contributions_router)
    app.include_router(incumbent_challenger_statuses_router)
    app.include_router(office_types_router)
    app.include_router(party_types_router)
    app.include_router(report_types_router)
    app.include_router(transaction_types_router)

    logger.info("completed application creation")
    return app
