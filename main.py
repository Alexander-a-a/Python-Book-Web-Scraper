import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize variables
current_page = 1
proceed = True
books = []  # List to store all the book details

while proceed:
    print(f"Currently scraping page {current_page}...")  # Status message for the current page
    url = f"https://books.toscrape.com/catalogue/page-{current_page}.html"

    # Make a request to the webpage
    try:
        page = requests.get(url)
        page.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve page {current_page}: {e}")
        break

    # Parse the webpage content
    soup = BeautifulSoup(page.text, "html.parser")

    # Check if the page is a 404 error (or similar)
    if soup.title and "404" in soup.title.text:
        proceed = False
        print(f"Stopping scraping. Page {current_page} does not exist.")
    else:
        all_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for book in all_books:
            item = {}  

            # Extract title, link, price, and stock information
            item["Title"] = book.find("img")["alt"]  # Title from image's alt attribute
            item["Link"] = book.find("a")["href"]  # Book link
            item["Price"] = book.find("p", class_="price_color").text.strip()[2:]  # Remove currency symbol
            item["Stock"] = book.find("p", class_="instock availability").text.strip()  # Stock status

            
            print(f"Title: {item['Title']}")
            print(f"Stock: {item['Stock']}")
            print(f"Price: {item['Price']}\n")

            books.append(item)  # Append book details to list

    current_page += 1  # Move to the next page


if books:
    df = pd.DataFrame(books)
    df.to_csv('books.csv', index=False)
    print("Scraping complete. Data saved to books.csv.")
else:
    print("No books found during the scraping process.")
