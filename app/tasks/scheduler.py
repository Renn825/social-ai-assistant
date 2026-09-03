from apscheduler.schedulers.background import BackgroundScheduler


def _scheduled_collection() -> None:
    # This is a deliberately small periodic job. Replace it with a real
    # collection or report-generation task after wiring MediaCrawler.
    pass


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        _scheduled_collection,
        trigger="interval",
        hours=24,
        id="daily_collection",
        replace_existing=True,
    )
    scheduler.start()
    return scheduler

