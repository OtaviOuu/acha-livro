from huey.contrib.djhuey import periodic_task
from huey import crontab
import requests
from parsel.selector import Selector
import requests_html

# quero importar modelo de busca
from .models import Termo

main_page_url = "https://www.estantevirtual.com.br/ciencias-exatas?sort=new-releases&tipo-de-livro=usado"
# https://www.estantevirtual.com.br/frdmprcsts/J92-9149-000/lazy


@periodic_task(crontab(minute="*/1"))
def every_minute():
    session = requests_html.HTMLSession()

    response = session.get(main_page_url)
    response.html.render(sleep=3, timeout=20)
    selector = Selector(text=response.html.html)

    books = selector.css(".product-item.product-list__item")
    all_terms = Termo.objects.all()
    print(len(all_terms), "termos encontrados")
    for book in books:
        book_title = book.css("a::attr(title)").get()
        print(f"Procurando livro: {book_title}")
        if book_title:
            for termo in all_terms:
                if termo.name.lower() in book_title.lower():
                    book_url = book.css("a::attr(href)").get()
                    book_image_url = book.css(
                        ".product-item__cover img::attr(src)"
                    ).get()

                    new_book_found = {
                        "name": book_title,
                        "url": book_url,
                        "image_url": book_image_url,
                    }
                    print(new_book_found)
                    termo.user.livros.append(new_book_found)
                    termo.user.save()
                    print(f"Livro encontrado: {book_title} para o termo {termo.name}")
