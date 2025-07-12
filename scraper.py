import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

def scrape_imdb_action_movies(url, genre):
    # This function is the same as the one you provided
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5) 
    movies_data = []
    movie_containers = driver.find_elements(By.CSS_SELECTOR, ".ipc-metadata-list-summary-item__c")
    for container in movie_containers:
        try:
            title_text = container.find_element(By.CSS_SELECTOR, ".ipc-title__text").text
            title = title_text.lstrip('0123456789. ')
        except NoSuchElementException:
            title = None
        metadata_items = container.find_elements(By.CSS_SELECTOR, ".dli-title-metadata-item")
        try:
            year = metadata_items[0].text if len(metadata_items) > 0 else None
        except IndexError:
            year = None
        try:
            duration = metadata_items[1].text if len(metadata_items) > 1 else None
        except IndexError:
            duration = None
        try:
            censor = metadata_items[2].text if len(metadata_items) > 2 else None
        except IndexError:
            censor = None
        try:
            rating_text = container.find_element(By.CSS_SELECTOR, "span.ipc-rating-star.ipc-rating-star--base").get_attribute('aria-label')
            rating = rating_text.replace('Rating: ', '')
        except (NoSuchElementException, AttributeError):
            rating = None
        try:
            vote_count = container.find_element(By.CSS_SELECTOR, ".ipc-rating-star--voteCount").text
        except NoSuchElementException:
            vote_count = None
        movies_data.append({
            'Title': title,
            'Year': year,
            'Duration': duration,
            'Censor': censor,
            'Rating': rating,
            'Vote Count': vote_count,
            'Genre': genre
        })
    driver.quit()
    return pd.DataFrame(movies_data)