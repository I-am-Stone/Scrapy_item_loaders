

<h1>Scrapy Overview</h1>

Scrapy is a fast, high-level web crawling and web scraping framework used to extract structured data from websites. It's versatile and can be used for data mining, monitoring, and automated testing. This project demonstrates how to utilize Scrapy item loaders to filter and process the data you need.

<h1>Requirements</h1>

- Python 3.8+
- Compatible with Linux, Windows, macOS, and BSD

Installation

To install Scrapy, run:

```bash
pip install scrapy
```

<h1>Documentation</h1>

For detailed documentation, visit the [official Scrapy documentation](https://docs.scrapy.org/en/latest/).

<h1>Item Loaders</h1>

Item loaders are used to filter and process the data extracted by Scrapy. Here’s a guide on how to use item loaders effectively.

<h1>How to Use Item Loaders</h1>

<h4>1. Define Item Fields</h4>

   In your `items.py` file, define the fields of your item and specify custom processors to clean and transform the data:

   ```python
   import scrapy
   from itemloaders.processors import TakeFirst, MapCompose
   from w3lib.html import remove_tags

   class MainItem(scrapy.Item):
       Course_Name = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip), output_processor=TakeFirst())
       Course_Description = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip))
       International_Fee = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, lambda x: x.replace('A$', 'AUD')), output_processor=TakeFirst())
       # Add more fields as needed
   ```

<h4>2. Use Item Loaders in Spiders</h4>

   In your spider, use the `ItemLoader` class to load and process data:

   ```python
   import scrapy
   from itemloaders.items import MainItem
   from scrapy.loader import ItemLoader

   class BurnSpider(scrapy.Spider):
       name = 'burnel'
       file_name = 'University of Brunel'

       def start_requests(self):
           urls = ['https://www.brunel.ac.uk/study/Course-listing?courseLevel=&page=0']
           for url in urls:
               yield scrapy.Request(url=url, callback=self.parse)

       def parse(self, response):
           courses = response.xpath('//table[contains(@id,"responsive-example-table")]//a/@href').getall()
           for course in courses:
               if course is not None:
                   yield response.follow(course, callback=self.parse_course)

           next_page = response.xpath('//ul[contains(@class,"pagination")]//a/@href').getall()
           for next in next_page:
               yield response.follow(next, callback=self.parse)

       def parse_course(self, response):
           loader = ItemLoader(item=MainItem(), response=response)
           loader.add_value('Course_Website', response.url)
           loader.add_xpath('Course_Name', '//title')
           loader.add_xpath('Duration', '//h3[contains(text(),"study")]/parent::div')
           loader.add_xpath('Duration_term', '//h3[contains(text(),"study")]/parent::div')
           loader.add_xpath('Study_Load', '//h3[contains(text(),"study")]/parent::div')
           # Add more fields and processing rules as needed

           yield loader.load_item()
   ```

<h4>3. Custom Processing Functions</h4>

   Define custom processing functions to clean or format the data:

   ```python
   def intake_clean(value):
       if value:
           return value.replace('Next intake', '').replace('is', '').strip()

   def clean_city(value):
       if value:
           return value.replace('Distance Learning', '').strip()

   def cn(value):
       return value.strip()

   class MainItem(scrapy.Item):
       Course_Website = scrapy.Field()
       Course_Name = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, cn), output_processor=TakeFirst())
       Course_Description = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip))
       Career = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
       City = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, clean_city))
       International_Fee = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, lambda x: x.replace('A$', 'AUD')), output_processor=TakeFirst())
       Domestic_Fee = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, lambda x: x.replace('A$', 'AUD')), output_processor=TakeFirst())
       Currency = scrapy.Field(input_processor=MapCompose(lambda x: x.strip()))
       Intake_Month = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, lambda x: x.strip()))
       Study_Load = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, lambda x: x.strip()))
   ```

<h4>4. Testing and Validation</h4>

   After configuring your item loaders, run your spider and check the output. Ensure the data is processed correctly and make necessary adjustments to item loader configurations or custom functions.

<h4>Conclusion</h4>

Scrapy item loaders help streamline data processing by allowing you to specify rules for transforming and cleaning scraped data. This approach ensures your dataset is well-organized and meets your project’s requirements. For more information and advanced usage, refer to the [Scrapy Item Loaders documentation](https://docs.scrapy.org/en/latest/topics/loaders.html).

By following this guide, you can effectively use item loaders to enhance your data extraction and processing tasks in Scrapy. you can ask me if you are stuck.....GG
