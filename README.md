<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scrapy Overview</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }
        h1 {
            background-color: #f4f4f4;
            padding: 1em;
            margin: 0;
        }
        ul {
            list-style-type: disc;
            margin: 1em 0;
            padding: 0 1em;
        }
        code {
            background-color: #f4f4f4;
            padding: 0.2em 0.4em;
            border-radius: 3px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 1em;
            border-radius: 3px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>Scrapy Overview</h1>
    <p>Scrapy is a fast, high-level web crawling and web scraping framework used to extract structured data from websites. It's versatile and can be used for data mining, monitoring, and automated testing. This project demonstrates how to utilize Scrapy item loaders to filter and process the data you need.</p>
    
    <h1>Requirements</h1>
    <ul>
        <li>Python 3.8+</li>
        <li>Compatible with Linux, Windows, macOS, and BSD</li>
    </ul>
    
    <h1>Installation</h1>
    <p>To install Scrapy, run:</p>
    <pre><code>pip install scrapy</code></pre>
    
    <h1>Documentation</h1>
    <p>For detailed documentation, visit the <a href="https://docs.scrapy.org/en/latest/">official Scrapy documentation</a>.</p>
    
    <h1>Item Loaders</h1>
    <p>Item loaders are used to filter and process the data extracted by Scrapy. Here’s a guide on how to use item loaders effectively.</p>
    
    <h2>How to Use Item Loaders</h2>
    
    <h3>1. Define Item Fields</h3>
    <p>In your <code>items.py</code> file, define the fields of your item and specify custom processors to clean and transform the data:</p>
    <pre><code>import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

class MainItem(scrapy.Item):
    Course_Name = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip), output_processor=TakeFirst())
    Course_Description = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip))
    International_Fee = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, lambda x: x.replace('A$', 'AUD')), output_processor=TakeFirst())
    # Add more fields as needed
</code></pre>
    
    <h3>2. Use Item Loaders in Spiders</h3>
    <p>In your spider, use the <code>ItemLoader</code> class to load and process data:</p>
    <pre><code>from scrapy.loader import ItemLoader
from myproject.items import MainItem

class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['http://example.com']

    def parse(self, response):
        loader = ItemLoader(item=MainItem(), response=response)
        loader.add_xpath('Course_Name', '//h1/text()')
        loader.add_xpath('Course_Description', '//div[@class="description"]/text()')
        loader.add_xpath('International_Fee', '//span[@class="fee"]/text()')
        # Add more fields and processing rules as needed

        yield loader.load_item()
</code></pre>
    
    <h3>3. Custom Processing Functions</h3>
    <p>Define custom processing functions to clean or format the data:</p>
    <pre><code>def clean_fee(value):
    return value.replace('A$', 'AUD').strip()

def clean_description(value):
    return value.replace('\n', ' ').strip()

class MainItem(scrapy.Item):
    Course_Name = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip), output_processor=TakeFirst())
    Course_Description = scrapy.Field(input_processor=MapCompose(remove_tags, clean_description))
    International_Fee = scrapy.Field(input_processor=MapCompose(remove_tags, clean_fee), output_processor=TakeFirst())
</code></pre>
    
    <h3>4. Testing and Validation</h3>
    <p>After configuring your item loaders, run your spider and check the output. Ensure the data is processed correctly and make necessary adjustments to item loader configurations or custom functions.</p>
    
    <h1>Conclusion</h1>
    <p>Scrapy item loaders help streamline data processing by allowing you to specify rules for transforming and cleaning scraped data. This approach ensures your dataset is well-organized and meets your project’s requirements. For more information and advanced usage, refer to the <a href="https://docs.scrapy.org/en/latest/topics/loaders.html">Scrapy Item Loaders documentation</a>.</p>
    <p>By following this guide, you can effectively use item loaders to enhance your data extraction and processing tasks in Scrapy.</p>
</body>
</html>
