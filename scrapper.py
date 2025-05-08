# python -m pip install requests
# => get data from web (html, json, xml)
# python -m pip install beautifulsoup4
# => parse html



# git init => initialize git
# git status  => if you want to check what are the status  of files
# git diff => if you want to check what are the changes
# git add .  => track  all files
# git commit -m "Your messagea" 

import json
import sqlite3
import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"


def create_table():
    con = sqlite3.connect("books.sqlite3")
    cur = con.cursor()
    cur.execute(
        """
            CREATE TABLE if not exists books(
                id integer primary key autoincrement,
                title text,
                price real,
                currency text
            );
        """
    )
    con.commit()
    con.close()



def insert_book(title, currency, price):
    con = sqlite3.connect("books.sqlite3")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO books (title, currency, price) VALUES (?, ?, ?)",
        (title, currency, price),
    )

    con.commit()
    con.close()  


def scrape_books(url):
    response = requests.get(url)
    # print(response.status_code)   # gives 200 which is get
    if response.status_code != 200:
        return []
    
    books = []
    
    # set encoding explicitly ro handle special characters correctly
    response.encoding = response.apparent_encoding
    
    # print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    book_elements = soup.find_all("article", class_ = "product_pod")

    for book in book_elements:
        title = book.h3.a['title']
        price_text = book.find("p", class_ = "price_color").text
        #print(title, price_text)  # price_text is of type string
        currency = price_text[0]
        price = float(price_text[1:])

        books.append(
            {"title": title,
             "currency" : currency,
             "price": price,
             }
        )

        # insert_book(title, currency, price)

    print("All books have beem scrapped and saved to database")
    return(books)


def save_to_json(books):
    import json
    
    with open("books.json", "w", encoding="utf-8") as f:   # encoding ani ensure_ascii le £ sign dekhaucha currency ma
        json.dump(books, f, indent=4, ensure_ascii=False)   # indent 4 books.json ramro dekhne banaucha, gap gap wala
    
    print("All books have been saved to books.json")



create_table()
books = scrape_books(URL)
save_to_json(books)