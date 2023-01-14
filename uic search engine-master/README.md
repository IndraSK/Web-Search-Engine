# UIC Web Search Engine

This project was done as the term project for CS582: Information Retrieval course at the University of Illinois at Chicago during the Fall2022 term.

The goal of the project is to design and implement a web search engine for the [UIC domain](https://www.uic.edu/). The search engine includes a web crawler, preprocessing and indexing of web pages, and an IR system implementing a vector-space model to retrieve webpages relevant to an input user query.

## Software Description

The software is designed in Python3.8, and all functions are modularized so that they can be extended further for use in other projects and future work. 

The search engine crawls, collects, and preprocesses 6000 webpages from the [UIC domain](https://www.uic.edu/), which takes around 3 hours to complete. 

So to execute the code without first crawling the UIC domain, all the pickle files needed to execute the code are included inside the PickleFiles folder. 

The search_query.py script file can be executed from the terminal to execute the search engine right away. However, the python scripts to execute the uic_crawler.py of web-pages and their preprocessor.py are also provided in the repository.

Detailed description of the various components and functionalities of the search engine can be found in the accompanying [project report](IR_Project_Report.pdf).


## Usage Details

To execute the web search engine, run the following command in the terminal:

`python search_query.py`

Similarly the python scripts to execute the uic_domain_crawler.py of web-pages and their preprocessor.py can also be executed from the terminal.
