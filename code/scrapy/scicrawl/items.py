# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ACLPaperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    anthology_id = scrapy.Field() # 去重
    volume = scrapy.Field()
    type = scrapy.Field()
    #month = scrapy.Field()
    date = scrapy.Field()
    year = scrapy.Field()
    venue = scrapy.Field() # 列表
    #date = scrapy.Field()
    citeThis = scrapy.Field() #暂不用
    pages = scrapy.Field()
    language = scrapy.Field()
    #url = scrapy.Field()
    doi = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field() # ['Lieke Gelderloos', 'Grzegorz Chrupała', 'Afra Alishahi']
    abstract = scrapy.Field()
    # pdf_url = scrapy.Field()
    pdf = scrapy.Field()
    pdf_path = scrapy.Field()
    inCitationsCount = scrapy.Field()
    outCitationsCount = scrapy.Field()
    venue_id = scrapy.Field()  #暂不用
    pdf_content_id = scrapy.Field()  #暂不用
    video_id = scrapy.Field()  #该阶段不用
    blog_id = scrapy.Field()  # 该阶段不用
    video_url = scrapy.Field()
    video_path = scrapy.Field()
    slide_url = scrapy.Field()
    slide_path = scrapy.Field()
    software_url = scrapy.Field()
    software_path = scrapy.Field()
    dataset_url = scrapy.Field()
    dataset_path = scrapy.Field()
    poster_url = scrapy.Field()
    poster_path = scrapy.Field()
    #other_attachments = scrapy.Field()
    dblp_mdate = scrapy.Field()
    dblp_id = scrapy.Field()
    # 表示清洗的时间，默认置为空字符串
    clean = scrapy.Field()

class ArxivPaperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    anthology_id = scrapy.Field() # 去重
    arxiv_id = scrapy.Field()
    volume = scrapy.Field()
    type = scrapy.Field()
    #month = scrapy.Field()
    date = scrapy.Field()
    year = scrapy.Field()
    venue = scrapy.Field() # 列表
    citeThis = scrapy.Field() #暂不用
    pages = scrapy.Field()
    language = scrapy.Field()
    #url = scrapy.Field()
    doi = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field() # ['Lieke Gelderloos', 'Grzegorz Chrupała', 'Afra Alishahi']
    abstract = scrapy.Field()
    # pdf_url = scrapy.Field()
    pdf = scrapy.Field()
    pdf_path = scrapy.Field()
    inCitationsCount = scrapy.Field()
    outCitationsCount = scrapy.Field()
    venue_id = scrapy.Field()  #暂不用
    pdf_content_id = scrapy.Field()  #暂不用
    video_id = scrapy.Field()  #该阶段不用
    blog_id = scrapy.Field()  # 该阶段不用
    video_url = scrapy.Field()
    video_path = scrapy.Field()
    slide_url = scrapy.Field()
    slide_path = scrapy.Field()
    software_url = scrapy.Field()
    software_path = scrapy.Field()
    dataset_url = scrapy.Field()
    dataset_path = scrapy.Field()
    poster_url = scrapy.Field()
    poster_path = scrapy.Field()
    #other_attachments = scrapy.Field()
    dblp_mdate = scrapy.Field()
    dblp_id = scrapy.Field()
    # 表示清洗的时间，默认置为空字符串
    clean = scrapy.Field()


class SciHubPaperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()

    doi = scrapy.Field()
    file_name = scrapy.Field()
    # title = scrapy.Field()


class ACMPaperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    # anthology_id = scrapy.Field() # 去重
    arxiv_id = scrapy.Field()
    volume = scrapy.Field()
    type = scrapy.Field()
    #month = scrapy.Field()
    date = scrapy.Field()
    year = scrapy.Field()
    venue = scrapy.Field() # 列表
    citeThis = scrapy.Field() #暂不用
    pages = scrapy.Field()
    language = scrapy.Field()
    #url = scrapy.Field()
    doi = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field() # ['Lieke Gelderloos', 'Grzegorz Chrupała', 'Afra Alishahi']
    abstract = scrapy.Field()
    # pdf_url = scrapy.Field()
    pdf = scrapy.Field()
    pdf_path = scrapy.Field()
    inCitationsCount = scrapy.Field()
    outCitationsCount = scrapy.Field()
    venue_id = scrapy.Field()  #暂不用
    pdf_content_id = scrapy.Field()  #暂不用
    video_id = scrapy.Field()  #该阶段不用
    blog_id = scrapy.Field()  # 该阶段不用
    video_url = scrapy.Field()
    video_path = scrapy.Field()
    slide_url = scrapy.Field()
    slide_path = scrapy.Field()
    software_url = scrapy.Field()
    software_path = scrapy.Field()
    dataset_url = scrapy.Field()
    dataset_path = scrapy.Field()
    poster_url = scrapy.Field()
    poster_path = scrapy.Field()
    #other_attachments = scrapy.Field()
    dblp_mdate = scrapy.Field()
    dblp_id = scrapy.Field()
    # 表示清洗的时间，默认置为空字符串
    clean = scrapy.Field()