import scrapy
from item_loders.items import MainItem
from scrapy.loader import ItemLoader





class burnSpider(scrapy.Spider):
    name='burnel'
    file_name='University of Brunel'


    def start_requests(self):
        urls=['https://www.brunel.ac.uk/study/Course-listing?courseLevel=&page=0']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        courses=response.xpath('//table[contains(@id,"responsive-example-table")]//a/@href').getall()
        
        for course in courses:
            if course is not None:
                yield response.follow(course, callback=self.parse1)

        next_page=response.xpath('//ul[contains(@class,"pagination")]//a/@href').getall()
        for next in next_page:
            yield response.follow(next, callback=self.parse)

    def parse1(self, response):

        Co=ItemLoader(item=MainItem(),response=response)

        Co.add_value('Course_Website',response.url)
        Co.add_xpath('Course_Name','//title')

        Co.add_xpath('Duration','//h3[contains(text(),"study")]/parent::div')
        Co.add_xpath('Duration_term','//h3[contains(text(),"study")]/parent::div')

        Co.add_xpath('Study_Load','//h3[contains(text(),"study")]/parent::div')
        

        Co.add_xpath('Course_Description','//h2[contains(text(),"Overview")]/parent::section//p')

        Co.add_xpath('Domestic_fee','(//p/strong[contains(text(),"UK")]//following-sibling::text())[2]')
        Co.add_xpath('International_Fee','(//p/strong[contains(text(),"Interna")]//following-sibling::text())[2]')
        Co.add_xpath('Intake_Month','//h3[contains(text(),"Start date")]/parent::div')
        Co.add_xpath('Course_Structure','//div[contains(@class,"sc-1270nyt-0 dWCTLk")]')


        Co.add_xpath('IELTS_Listening','//li[contains(text(),"IELTS")]')
        Co.add_xpath('IELTS_Speaking','//li[contains(text(),"IELTS")]')
        Co.add_xpath('IELTS_Writing','//li[contains(text(),"IELTS")]')
        Co.add_xpath('IELTS_Overall','//li[contains(text(),"IELTS")]')
        Co.add_xpath('IELTS_Reading','//li[contains(text(),"IELTS")]')

        Co.add_xpath('PTE_istening','//li[contains(text(),"Pearson")]')
        Co.add_xpath('PTE_Speaking','//li[contains(text(),"Pearson")]')
        Co.add_xpath('PTE_Writing','//li[contains(text(),"Pearson")]')
        Co.add_xpath('PTE_Reading','//li[contains(text(),"Pearson")]')
        Co.add_xpath('PTE_Overall','//li[contains(text(),"Pearson")]')

        Co.add_xpath('TOEFL_Speaking','//li[contains(text(),"TOEFL")]')
        Co.add_xpath('TOEFL_Writing','//li[contains(text(),"TOEFL")]')
        Co.add_xpath('TOEFL_Listening','//li[contains(text(),"TOEFL")]')
        Co.add_xpath('TOEFL_Reading','//li[contains(text(),"TOEFL")]')
        Co.add_xpath('TOEFL_Overall','//li[contains(text(),"TOEFL")]')




        infee=response.xpath('(//p/strong[contains(text(),"Interna")]//following-sibling::text())[2]').get()
        dofee=response.xpath('(//p/strong[contains(text(),"UK")]//following-sibling::text())[2]').get()

        Co.add_value('Fee_term','Year') if infee or dofee else ""
        Co.add_value('Fee_year','2023') if infee or dofee else ""
        Co.add_value('Currency','GBP')  if infee or dofee else ""


        yield Co.load_item()




