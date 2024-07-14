
import scrapy
from item_loders.items import MainItem
from scrapy.loader import ItemLoader


class stanelySpider(scrapy.Spider):
    name='stan'
    file_name='Stanley_college'
    start_urls=['https://www.stanleycollege.edu.au/']

    def parse(self, response):
        depart=response.xpath('//div[contains(@class,"col-md-3 p-1")]/a/@href').getall()
        for cour in depart:
            if cour is not None:
                yield response.follow(cour, callback=self.parse_link)
    
    def parse_link(self, response):
        all_courses=[]
        courses=response.xpath('//div[contains(@class,"course-whiteprt")]/a/@href').getall()
        bachelor=response.xpath('//h2[contains(@class,"course-title")]//a/@href').getall()
        all_courses.extend(courses)
        all_courses.extend(bachelor)

        for course in all_courses:
            if course is not None:
                yield response.follow(course, callback=self.parse2)


    def parse2(self, response):
        Co=ItemLoader(item=MainItem(),response=response)

        Co.add_value('Course_Website',response.url)
        Co.add_xpath('Course_Name','//div[contains(@class,"bechlomin")]//h1')
        Co.add_xpath('Duration','//strong[contains(.,"Duration:")]//following-sibling::text()')
        Co.add_xpath('Duration_Term','//strong[contains(.,"Duration:")]//following-sibling::text()')
        Co.add_xpath('Study_mode','//strong[contains(.,"Study Mode:")]//following-sibling::text()')
        Co.add_xpath('Intake_Month','//strong[contains(.,"Intake Dates:")]/following-sibling::text()')
        Co.add_xpath('City','//strong[contains(.,"Location:")]/following-sibling::text()')

        Co.add_xpath('Domestic_fee','(//strong[contains(.,"Domestic Students")]//following-sibling::text())[1]')

        Co.add_xpath('International_Fee','(//strong[contains(.,"International")]//following-sibling::text())[1]')
        infee=response.xpath('(//strong[contains(.,"International")]//following-sibling::text())[1]').get()
        dofee=response.xpath('(//strong[contains(.,"Domestic Students")]//following-sibling::text())[1]').get()
        Co.add_xpath('Course_Description','//h2[contains(.,"Course Overview")]//following-sibling::p')


        Co.add_value('Fee_Term','Year') if infee or dofee else ""
        Co.add_value('Fee_Year','2023') if infee or dofee else ""
        Co.add_value('Currency','GBP')  if infee or dofee else ""

        yield Co.load_item()


        
        
        

        