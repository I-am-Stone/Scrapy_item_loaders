# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
class ItemLodersPipeline:

    def __init__(self):
        self.items= []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        try:
            df.sort_values(by="Course_Name", axis=0,
                           inplace=True, ascending=True)
        except:
            print("error")      
        df.to_excel("excle_file/" + spider.file_name +  # "v1" +
                        ".xlsx", index=False)
        print("Item exported sucessfully")