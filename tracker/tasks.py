from celery import shared_task


@shared_task
def scrape():
    print("Scraping started")
