## scraper.py

- Description: scrape a web url
- Input: url
- It will download the source

- It will do some cleanup:

1. remove all content in <head>, except titile part
2. remove all css code, and any link to stylesheet file
3. remove all script code, and any link to script file

- Output:

1. text file, with name "{url}.txt"
2. saved in "out" folder. Create it if not exist
