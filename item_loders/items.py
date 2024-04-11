# # Define here the models for your scraped items
# #
# # See documentation in:
# # https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import re








def intake_clean(value):
     if value is not None:
          value.replace('Next intake','').replace('is','')
          return value




def clean_city(value):
     if value is not None:
          value.replace('Distance Learning','')
          return value
def cn(value):
     return value.strip()


def mode(value):
      if value is not None:
            value='Both' if value.find("/") != -1 else ('Online' if value.find('Online')!= -1 else 'On Campus')
            return value


def clean_dur(value):
      if value is not None:
            return value.replace('years','').strip()

def clean_space(value):
        if value is not None:
            value = re.sub(r'^\s+|\s+$', '', value)
            return value
        
def clean_numbers(value):
        if value is not None:
            value = re.sub(r'\d+', '', value)
            return value
        
def Currency_clean(value):
      if value is not None:
            return value.replace('A$','AUD').replace('AU$','').replace('* fee per semester','').strip()
      
def study(value):
     if value:
          if u"Full-time" in value and u"Part-time" in value:
               return "Both"
          if u"Part-time" in value or u"(part time)" in value:
               return "Part Time"
          if u"Full-time" in value or u"(full time)" in value:
               return "Full Time"


def clean(value):
     if value is not None:
          return value.replace('2:2','').replace('32-48','')



def iltes_overall(value):
    try:
          main=clean(value)
          values = re.findall(r'\d+\.*\d*', main)
          overall=values[0]
          return overall
    except:
         pass


def couse_clean(value):
     if value is not None:
          return value.replace("20 credits","")


def iltes_all(value):
     try:
          main=clean(value)
          values = re.findall(r'\d+\.*\d*', main)
          size=len(values)
          if size < 3:
               overall=values[1]
               return overall
          else:
               overall=values[2]
               return overall
     except:
         pass
    
def iltes_write(value):
     try:
               main=clean(value)
               values = re.findall(r'\d+\.*\d*', main)
               big=len(values)
               if big < 3:
                    overall=values[1]
                    return overall
               else:
                    overall=values[1]
                    return overall
     except:
          pass
             
    
def term_du(value):
     if value is not None:
          value = "Year" if value.find("years") != -1 else ("Month" if value.find("months") != -1 else (
                "Week" if value.find("weeks") != -1 else ("Day" if value.find("day") != -1 else (
                    "Hour" if value.find("hours") != -1 else (
                        "Semester" if value.find("semester") != -1 else ("Year" if value.find("year") != -1 else ("Year" if value.find("Year")!= -1 else "")))))))
          return value



def dura(value):
     if value is not None:
          value = "3" if value.find("Three") != -1 else ("4" if value.find("four ") != -1 else (
                "1" if value.find("One") != -1 else ("2" if value.find("Two") != -1 else ("1" if value.find("1") != -1 else ("12" if value.find("12") != -1 else('6' if value.find(6) != -1 else ''))))))
          return value


def dur_clean(value):
     try:
        value.replace('full time to equivalent','')
        

        an_du=value.find('to') or value.find(' - ')
        if an_du != -1:
            one=re.findall(r'\d+\.*\d*', value)
            return "{} to {}".format(one[0],one[1])
            
            

        value = re.findall(r'\d+\.*\d*', value)
        duration=value[0]
        return duration
     except:
          pass



def fee_clean(value):
     if value is not None:
          return value.replace('Year 1:','').replace('2023/24','')

def fees(value):
     try:
        main=fee_clean(value)
        re_main = re.findall(r'\d+,*\d*', main)
        fees=re_main[0]
        return fees
     except:
          pass

def TOEFL_Overall(value):
    value = re.findall(r'\d+', value)
    overall=value[0]
    return overall

def TOEFL_all(value):
     value = re.findall(r'\d+', value)
     overall=value[1]
     return overall


def pteall(value):
    value = re.findall(r'\d+', value)
    overall=value[1]
    return overall

def pte_overall(value):
    value = re.findall(r'\d+', value)
    overall=value[0]
    return overall





class MainItem(scrapy.Item):
     Course_Website = scrapy.Field()
     Course_Name = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,cn), output_processor= TakeFirst())
     Course_Description = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space))
     Career = scrapy.Field(input_processor = MapCompose(clean_space), output_processor= TakeFirst())
     City = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,clean_city))
     International_Fee = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,fee_clean,fees), output_processor= TakeFirst())
     Domestic_fee = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,fee_clean,fees), output_processor= TakeFirst())
     Currency = scrapy.Field()
     Intake_Month = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,clean_numbers), output_processor= TakeFirst())
     Study_Load = scrapy.Field(input_processor = MapCompose(remove_tags,clean_numbers,clean_space,study))
     Duration_Term = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,clean_numbers,term_du), output_processor= TakeFirst())
     Fee_Term= scrapy.Field()
     Duration= scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,dur_clean), output_processor= TakeFirst())
     Study_mode = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space), output_processor= TakeFirst())
 
     IELTS_Listening = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space, iltes_all),output_processor= TakeFirst())
     IELTS_Speaking = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space, iltes_all),output_processor= TakeFirst())
     IELTS_Writing = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space, iltes_all),output_processor= TakeFirst())
     IELTS_Reading = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space, iltes_all),output_processor= TakeFirst())
     IELTS_Overall = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space, iltes_overall),output_processor= TakeFirst())

     TOEFL_Speaking = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,TOEFL_all),output_processor= TakeFirst())
     TOEFL_Writing = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,TOEFL_all),output_processor= TakeFirst())
     TOEFL_Listening = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,TOEFL_all),output_processor= TakeFirst())
     TOEFL_Reading = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,TOEFL_all),output_processor= TakeFirst())
     TOEFL_Overall = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,TOEFL_Overall),output_processor= TakeFirst())

     PTE_istening = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,pteall), output_processor= TakeFirst())
     PTE_Speaking = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,pteall), output_processor= TakeFirst())
     PTE_Writing = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,pteall), output_processor= TakeFirst())
     PTE_Reading = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,pteall), output_processor= TakeFirst())
     PTE_Overall = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space,pte_overall), output_processor= TakeFirst())
     Course_Structure=scrapy.Field(input_processor = MapCompose(clean_space, couse_clean))
   
    
     English_Test = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space), output_processor= TakeFirst())
     English_Test_Reading = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space), output_processor= TakeFirst())
     English_Test_Listening = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space), output_processor= TakeFirst())
     English_Test_Speaking = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space), output_processor= TakeFirst())
     English_Test_Writing = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space), output_processor= TakeFirst())
     English_Test_Overall = scrapy.Field(input_processor = MapCompose(remove_tags,clean_space), output_processor= TakeFirst())
    
    
     Category = scrapy.Field()
     Sub_Category = scrapy.Field()
     Other_Requriment= scrapy.Field()
     Apply_Day = scrapy.Field()
     Apply_Month = scrapy.Field()
     Fee_Year=scrapy.Field()
     Intake_Day = scrapy.Field()
     Language = scrapy.Field()
     Degree_level=scrapy.Field()
     Language=scrapy.Field()
     Academic_Level = scrapy.Field()
     Domestic_only=scrapy.Field()
     Other_Test = scrapy.Field()
     Academic_Score = scrapy.Field()
     Score_Type = scrapy.Field()
     Academic_Country = scrapy.Field()
     Score = scrapy.Field()
     Scholarship = scrapy.Field()

    



