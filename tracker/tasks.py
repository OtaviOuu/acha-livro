from celery import shared_task
from parsel.selector import Selector
from requests_html import HTMLSession


main_page_url = "https://www.estantevirtual.com.br/ciencias-exatas?sort=new-releases&tipo-de-livro=usado"
# https://www.estantevirtual.com.br/frdmprcsts/J92-9149-000/lazy


@shared_task
def scrape():
    session = HTMLSession()
    response = session.get(main_page_url)
    response.html.render(timeout=20, sleep=5)  #

    rendered_html = response.html.html
    selector = Selector(text=rendered_html)

    books_titles = selector.css(
        "#product-item .product-item__link.smarthint-tracking-card::attr(title)"
    ).getall()

    for boook in books_titles:
        print(boook)
