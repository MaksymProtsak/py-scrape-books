from typing import List
from urllib.parse import urljoin

import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"

    def start_requests(self):
        urls = [
            "https://books.toscrape.com/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, *args, **kwargs):
        books = response.css(".product_pod")
        next_page_url = response.css(".next").css("a::attr(href)").get()
        for book in books:
            book_ulr = book.css("h3").css("a::attr(href)").get()
            book_full_url = urljoin(response.url, book_ulr)
            yield scrapy.Request(url=book_full_url, callback=self.parse_book)

    def parse_book(self, response, *args, **kwargs):
        product_main = response.css(".product_main")
        title = product_main.css("h1::text").get()
        price = float(product_main.css(
            ".price_color::text"
        ).get().replace("£", ""))
        amount_in_stock_text_list = product_main.css(
            ".instock.availability::text"
        ).getall()
        amount_in_stock = self.get_b_n_from_stock_l(
            amount_in_stock_text_list
        )
        rating = ""
        breakpoint()

    @staticmethod
    def get_b_n_from_stock_l(stock_list: List) -> int:
        """
        Get book number from stock list
        :param stock_list:
        :return int:
        """
        stock_str = "".join(
            [
                char
                for char in "".join(stock_list)
                if char.isdigit()
            ]
        )
        return int(stock_str)
