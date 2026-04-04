import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from application.use_cases.check_stock import CheckStockUseCase
from infrastructure.config import load_settings
from infrastructure.notifiers.slack import SlackNotifier
from infrastructure.notifiers.telegram import TelegramNotifier
from infrastructure.persistence.sqlite_repo import SQLiteObservationRepository
from infrastructure.retailers.canyon.retailer import CanyonRetailer

# Setup structured logging
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    cache_logger_on_first_use=True,
)
logger = structlog.get_logger()

# Global state
settings = load_settings("config.toml")
repository = SQLiteObservationRepository(settings.sqlite_path)
retailer = CanyonRetailer()

notifiers = []
if settings.notifications.telegram.enabled:
    notifiers.append(
        TelegramNotifier(
            settings.notifications.telegram.bot_token,
            settings.notifications.telegram.chat_id,
        )
    )
if settings.notifications.slack.enabled:
    notifiers.append(SlackNotifier(settings.notifications.slack.webhook_url))

check_stock_use_case = CheckStockUseCase(retailer, repository, notifiers)
scheduler = AsyncIOScheduler()


async def run_checks():
    """Trigger stock checks for all enabled targets."""
    for target in settings.targets:
        if not target.enabled:
            continue

        logger.info("Checking stock", target_id=target.id, name=target.name)
        try:
            observation = await check_stock_use_case.execute(target)
            logger.info(
                "Stock check complete",
                target_id=target.id,
                state=observation.state.value,
                is_buyable=observation.is_buyable,
            )
        except Exception as e:
            logger.exception("Stock check failed", target_id=target.id, error=str(e))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Canyon Stock Monitor")

    # Ensure data directory exists
    Path(settings.sqlite_path).parent.mkdir(parents=True, exist_ok=True)

    # Start scheduler
    scheduler.add_job(
        run_checks,
        "interval",
        seconds=settings.app.poll_interval_seconds,
        id="check_all_targets",
        replace_existing=True,
    )
    scheduler.start()

    # Initial check
    asyncio.create_task(run_checks())

    yield

    # Shutdown
    logger.info("Shutting down")
    scheduler.shutdown()


app = FastAPI(title="Canyon Stock Monitor", lifespan=lifespan)


@app.get("/health/live")
async def liveness():
    return {"status": "ok"}


@app.get("/health/ready")
async def readiness():
    # Basic check if we can query the repo
    try:
        repository.get_latest("health-check")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 503


@app.get("/monitors")
async def list_monitors():
    results = []
    for target in settings.targets:
        latest = repository.get_latest(target.id)
        results.append({"target": target, "latest_observation": latest})
    return results


@app.get("/monitors/{target_id}")
async def get_monitor(target_id: str):
    target = next((t for t in settings.targets if t.id == target_id), None)
    if not target:
        return {"error": "Target not found"}, 404

    latest = repository.get_latest(target_id)
    return {"target": target, "latest_observation": latest}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
