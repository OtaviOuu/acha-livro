from huey.contrib.djhuey import periodic_task
from huey import crontab
from parsel.selector import Selector
import requests_html

# quero importar modelo de busca
from .models import Termo
from urllib.parse import urljoin
from seleniumbase import SB

main_page_url = "https://www.estantevirtual.com.br/ciencias-exatas?sort=new-releases&tipo-de-livro=usado"
# https://www.estantevirtual.com.br/frdmprcsts/J92-9149-000/lazy


@periodic_task(crontab(minute="*/1"))
def every_minute():
    with SB(uc=False, headless=False) as sb:
        sb.get(main_page_url)
        sb.wait(seconds=3)
        sb.slow_scroll_to(".payment-flags__title", timeout=10)
        sb.slow_scroll_to()
        html = sb.get_page_source()

    selector = Selector(text=html)

    books = selector.css(".product-item.product-list__item")
    all_terms = Termo.objects.all()
    print(len(all_terms), "termos encontrados")
    for book in books:
        book_title = book.css("a::attr(title)").get()
        if book_title:
            for termo in all_terms:
                if termo.name.lower() in book_title.lower():
                    book_href = book.css("a::attr(href)").get()
                    book_url = (
                        urljoin("https://www.estantevirtual.com.br", book_href)
                        if book_href
                        else None
                    )
                    book_image_url = book.css("img::attr(src)").get()

                    new_book_found = {
                        "name": book_title,
                        "url": book_url,
                        "image_url": book_image_url,
                    }

                    if new_book_found in termo.user.livros:
                        print("Livro já registrado")
                        continue

                    termo.user.livros.append(new_book_found)
                    termo.user.save()
