## Exercise

You are tasked with creating a data-processing app that pre-processes and enrich the data coming from crawlers, with the following requirements.

INPUT: csv-like data submitted by crawlers
OUTPUT: clean data in mongodb collections

1. The app is an HTTP API, every year, crawlers will submit the data saved in a file using an API endpoint designed by you.
2. Examples of data the crawlers will submit every year, see `data-2018.txt`, `data-2019.txt`, `data-2020.txt`. You can't change the format of the data.
3. As you can see, the data coming from crawlers is not 100% well-structured, the API should parse it correctly.
4. if there is any error in the submission, the API should return a proper error message with proper HTTP response status
4. For each university, enrich the data with a URL and a text description of it using Duckduckgo API
e.g. https://api.duckduckgo.com/?q=harvard&format=json&pretty=1
5. The app inserts or updates **clean** data in 3 mongodb tables/collections:

 * table 1 - the yearly data table
 * table 2 - the university table
 * table 3 - the top university in each country

"top" is defined as the university with the highest "Alumni Employment" score

6. the data processing and transformations should be covered by tests
