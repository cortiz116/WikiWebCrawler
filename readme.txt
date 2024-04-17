# ChristianaOrtizFinal1250
# Programmer: Christiana Ortiz
# Email: cortiz116@cnm.edu
# Purpose: Description, requirements, and data structure for Six Degrees program
# Python version 3.12

# Description
The Six Degrees of Separation program allows a user to select a Wikipedia article from a list,
then uses the Wikipedia API and a web scraper to create a chain of links, creating a sort of digital version of the
Six Degrees of Separation theory or Six Degrees of Kevin Bacon game.

# Required libraries
wikipediaapi
random
requests
bs4
tkinter
re

Created using PyCharm 2023.3.2

# Data Structure

The starting_pages list contains the user's choices for the starting article:
    starting_pages = [
    "Separation of powers",
    "Kevin Bacon",
    "Fahrenheit",
    "Celsius",
    "98 Degrees",
    ]

The all_links set is created when each article is searched for all html <a> tags (denoting hyperlinks).

This set is used to filter the links to exclude external and other irrelevant links.
The remaining links are stored in the wikipedia_links list:
    wikipedia_links = [
            link['href']
            for link in all_links
            if re.match(r'^/wiki/[^:]*$', link['href'])
            and not any(substring in link['href'] for substring in
                        ['/File:', '/Category:', '/Help:', '/Special:', '/Template:', '/Portal:', '/Talk:',
                        '/User:', '/wiki/Template:'])
    ]

The chain of randomly chosen links is stored in an initially empty list called links.
This list is output to the user in a textbox.