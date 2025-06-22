from huey.contrib.djhuey import periodic_task
from huey import crontab
import requests
from parsel.selector import Selector
import requests_html

main_page_url = "https://www.estantevirtual.com.br/ciencias-exatas?sort=new-releases&tipo-de-livro=usado"
# https://www.estantevirtual.com.br/frdmprcsts/J92-9149-000/lazy


@periodic_task(crontab(minute="*/1"))
def every_minute():
    session = requests_html.HTMLSession()

    response = session.get(main_page_url)
    response.html.render(sleep=1, timeout=20)
    selector = Selector(text=response.html.html)
    titles = selector.css(
        ".product-item__link.smarthint-tracking-card::attr(title)"
    ).getall()
    for title in titles:
        print(title)
