# ChristianaOrtizFinal1250
# Programmer: Christiana Ortiz
# Email: cortiz116@cnm.edu
# Purpose: A Six Degrees of Separation program using a Wikipedia web scraper
# Python version 3.12

# Libraries
import wikipediaapi
import random
import requests
from bs4 import BeautifulSoup
from tkinter import *
import re

# Specify user_agent string per WikiMedia policy
user_agent = 'WikiWebCrawler/1.0 (cortiz116@cnm.edu)'

"""
get_links function gets user's choice of starting page, gets a chain of six random links, and returns the list of links
"""


def get_links(page_title, num_links):
    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)
    base_url = 'https://en.wikipedia.org/wiki/'

    # Get the starting page
    starting_page = wiki_wiki.page(page_title)

    # Initialize list and current page variable
    links = []
    current_page = starting_page

    # Crawl through links
    for _ in range(num_links - 1):
        # Construct the URL for the current page
        current_url = base_url + current_page.title.replace(' ', '_')

        # Fetch HTML content of the current page
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the links on the page
        all_links = soup.find_all('a', href=True)

        # Filter out internal Wikipedia links
        wikipedia_links = [
            link['href']
            for link in all_links
            if re.match(r'^/wiki/[^:]*$', link['href'])
            and not any(substring in link['href'] for substring in
                        ['/File:', '/Category:', '/Help:', '/Special:', '/Template:', '/Portal:', '/Talk:',
                        '/User:', '/wiki/Template:'])
        ]

        if not wikipedia_links:
            print(f"Sorry, the chain could not be completed. Please try again.")
            break

        # Get a random link from the current page
        random_link = random.choice(wikipedia_links)

        # Get the page title from the random link
        page_title = random_link.split('/')[-1].replace('_', ' ')

        # Set the current page to the random Wikipedia link for the next iteration
        current_page = wiki_wiki.page(page_title)

        # Add the random link to the list
        links.append(current_page.title)

    return links


# GUI with dropdown menu
# Create object
root = Tk()
root.title("Six Degrees of Separation Wikipedia API Scraper")

# Adjust size
root.geometry("800x400")

# Create description label
label = Label(root, text="This program uses a Wikipedia API scraper "
                         "\nto create a chain of six links from a starting article."
                         "\n\nChoose an article from the menu to begin.")
label.pack(pady=5)


'''
start_process function gets user selection and sets it as the starting page, clears the output text box,
gets the list of links from the get_links function and formats the output
'''


def start_process():

    starting_page = dropdown.get()  # Get user selection
    output_text.delete(1.0, END)  # Clear previous text
    links = get_links(starting_page, 7)  # Get list of links from get_links
    if links:
        output_text.insert(END, f"Six degrees of {starting_page}:\n\n")
        for link in links:
            output_text.insert(END, f"{link}\n")
    else:
        output_text.insert(END, "Sorry, the chain could not be completed. Please try again.")


# Starting pages dropdown menu
starting_pages = [
    "Separation of powers",
    "Kevin Bacon",
    "Fahrenheit",
    "Celsius",
    "98 Degrees",
]
dropdown = StringVar(root)
dropdown.set("Six degrees of...")  # Set default option
dropdown_menu = OptionMenu(root, dropdown, *starting_pages)
dropdown_menu.pack(pady=10)

# Create start button
button = Button(root, text="Start", command=start_process)
button.pack(pady=5)

# Create output textbox
output_text = Text(root, height=10, width=80)
output_text.pack(pady=10)

# Execute
root.mainloop()
