# Generic Web Scraper

This web scraper is designed to collect data about the biggest discounts from the Steam Online store and save the data in a configured output csv file. It can also be configured to collect any type of data. It is written in Python and based on selectolax and PlayWright.

## Configuration file

There are a lot of options to configure the program:

* **"url"**: The url from where to scrape data.
* **"output_file"**: The location of where to save the data.
* **"container"**: The main container for data (in this case, the div that stores the information for every game). The container also has more configuration settings:
    * **"name"**: Not important for the program, just for ease of reading.
    * **"selector"**: The format for the CSS selector ("https://www.w3schools.com/cssref/css_selectors.php" for more information).
    * **"match"**: Can take the values of "all", so all matches will be saved, or "first", so only the first occurence is saved
    * **"type"**: Can take the values of "node" to save the found tags as nodes, "text" to get the text attribute of the tag, or any other attribute (ex: "src" of an img tag to get the source url of the image)
* **"item"**: A list of items to get from every container with the same settings as the container. The difference is in the **"name"** setting, which will be used as a column name in the final csv file

## Installation

To install the required packages, run the **install.sh** script in a bash terminal.

### Demonstration run with jupyter notebook

To test the program, type **jupyter notebook** in the terminal and wait until the server is started. To access the notebook, go to **https://localhost:8888/tree** and go to the **"Scraper.ipynb"** notebook.

### Running the web scraper

To run the web scraper, type **python3 scraper.py** in the terminal.