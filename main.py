import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for, redirect, request
import pandas as pd
import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def my_form_post():
    prod_name = request.form['prod_name']
    headers = {
        "Accept-Language": 'en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    final_products = []

    amazon_response = requests.get(
        f'https://www.amazon.in/s?k={prod_name}&crid=3L97IGIXR8RP9&sprefix=oculus%2Caps%2C211&ref=nb_sb_noss_1',
        headers=headers).text
    amazon_soup = BeautifulSoup(amazon_response, 'html.parser')

    raw_product_images = amazon_soup.find_all(name='img', class_='s-image')
    final_product_images = []

    for n in raw_product_images:
        final_product_images.append(n.get('src'))


    # getting the stars for the product
    raw_product_stars = amazon_soup.select(selector='.a-icon-star-small span')
    final_product_stars = []

    for i in raw_product_stars:
        final_product_stars.append(i.getText())

    # getting the titles of the products
    raw_product_titles = amazon_soup.select(selector='.a-link-normal .a-text-normal')
    final_product_titles = []

    for i in raw_product_titles:
        final_product_titles.append(i.getText())

    # getting the dates of delivery of the product
    raw_delivery_dates = amazon_soup.select(selector='.s-align-children-center span .a-text-bold')
    final_delivery_dates = []
    for date in raw_delivery_dates:
        final_delivery_dates.append(date.getText())

    # getting the number of ratings of the product
    raw_number_ratings = amazon_soup.select(selector='.a-spacing-top-micro .a-row .a-size-base')
    final_number_ratings = []
    for ratings in raw_number_ratings:
        final_number_ratings.append(ratings.getText())

    # getting price of the products
    raw_product_price = amazon_soup.select(selector='.a-section .a-size-base a .a-price span .a-price-whole')
    final_product_prices = []
    for i in raw_product_price:
        final_product_prices.append(i.getText())
    # getting the links of the products
    raw_product_links = amazon_soup.find_all(name='a',
                                             class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    final_product_links = []
    for i in raw_product_links:
        final_product_links.append(f"https://amazon.in{i.get('href')}")

    for i in range(len(final_product_links)):
        try:
            final_products.append(
                {
                    'image': final_product_images[i],
                    'title': final_product_titles[i],
                    'price': final_product_prices[i],
                    'stars': final_product_stars[i],
                    'date': final_delivery_dates[i],
                    'ratings': final_number_ratings[i],
                    'links': final_product_links[i]
                }
            )
        except IndexError:
            pass
    return render_template("result.html", final_products_list=final_products)


if __name__ == "__main__":
    app.run(debug=True)
