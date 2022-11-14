# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinItem(scrapy.Item):
    # define the fields for your item here like:
    job_title = scrapy.Field()
    company_name = scrapy.Field()
    company_linkedin_link = scrapy.Field()
    company_location = scrapy.Field()
    company_image = scrapy.Field()
    work_method = scrapy.Field()
    post_date = scrapy.Field()
    applicants = scrapy.Field()
    work_time = scrapy.Field()
