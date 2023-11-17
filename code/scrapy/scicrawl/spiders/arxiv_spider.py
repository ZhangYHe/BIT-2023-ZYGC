import scrapy
from scicrawl.items import ArxivPaperItem
import yaml
from urllib.parse import urljoin
import logging
import os
from bson import ObjectId
#from utils.sendEmail import ErrorEmail
from utils.logger import logger

# logging_config_file = './logging_config.yaml'
#
# # 设置日志
# with open(logging_config_file, 'r') as f:
#     config = yaml.safe_load(f.read())
#     config['handlers']['file']['filename'] += "_arxivspider.log"
#     config['handlers']['info_file_handler']['filename'] += "_arxivspider.log"
#     print(config)
#     logging.config.dictConfig(config)
#     f.close()
# logger = logging.getLogger(__name__)

class ArxivSpider(scrapy.Spider):
    name = 'arxivspider'
    allowed_domains = ['arxiv.org']
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'DOWNLOAD_DELAY': 2,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 3
    }

    def __init__(self):
        # 从91年开始： https://arxiv.org/list/[domains]/[year+month]  # 无需通过这种方式
        # https://arxiv.org/list/astro-ph/9204
        self.domains = ['cs', 'astro-ph', 'cond-mat', 'econ', 'eess', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th',
                    'math', 'nlin', 'nucl-ex', 'nucl-th', 'physics', 'q-bio', 'q-fin', 'quant-ph', 'stat']
        self.domain_id = 0
        self.base_url = "https://arxiv.org/archive/"
        self.domain_url = self.base_url + self.domains[0]
        self.start_urls = [self.domain_url]
        #self.email = ErrorEmail()

    def parse(self, response):
        logger.info('Crawling ' + self.domain_url)

        # https://arxiv.org/archive/cs
        years = response.xpath("/html/body[@class='with-cu-identity']/div[@class='flex-wrap-footer']/main/div[@id='content']/ul[1]/li[4]/a/@href").extract()
        for year in years:
            # https://arxiv.org/year/cs/22
            year_url = urljoin("https://arxiv.org",year)
            yield scrapy.Request(year_url, callback=self.parseYear)

        logger.info('Finished ' + self.domain_url)

        if self.domain_id < len(self.domains) - 1:
            # 处理下一个domain
            self.domain_id += 1
            self.domain_url = self.base_url + self.domains[self.domain_id]
            yield scrapy.Request(self.domain_url, callback=self.parse)

    def parseYear(self, response):
        months = response.xpath("/html/body[@class='with-cu-identity']/div[@id='content']/ul/li/a[1]/@href").extract()

        for month in months:
            # https://arxiv.org/list/cs/2201
            month_url = urljoin("https://arxiv.org",month)
            yield scrapy.Request(month_url, callback=self.parseEntry)

    def parseEntry(self, response):
        entries = response.xpath("/html/body[@class='with-cu-identity']/div[@id='content']/div[@id='dlpage']/small[1]/text()").extract()
        # [ total of 5507 entries:  1-25 | 26-50 | 51-75 | 76-100 | ... | 5501-5507

        # 没有论文 TODO
        if entries is None:
            yield

        # 匹配entries数目
        entries_b = entries[0].find("of ")
        entries_e = entries[0].find(" entries")
        entries_num = int(entries[0][entries_b+3:entries_e])
        # /list/cs/2201?skip=25&show=25
        if entries_num>50:
            ebase_url = response.xpath("/html/body[@class='with-cu-identity']/div[@id='content']/div[@id='dlpage']/small[1]/a/@href").extract()[0].split("?")[0]
            #print(ebase_url)
            for i in range(entries_num%50):
                # https://arxiv.org/list/cs/2201?skip=0&show=50
                paperlist_url = 'https://arxiv.org' + ebase_url + "?skip=%s&show=%s" % (str(i*50),str((i+1)*50))
                #print(paperlist_url)
                # 在self.parseEntryList中处理所有页面
                yield scrapy.Request(paperlist_url, callback=self.parseEntryList)
        # 只有1页
        else:
            papers = response.xpath("/html/body[@class='with-cu-identity']/div[@id='content']/div[@id='dlpage']/dl/dt/span[@class='list-identifier']/a[1]/@href").extract()
            for paper in papers:
                paper_url = urljoin('https://arxiv.org', paper)
                yield scrapy.Request(paper_url, callback=self.parsePaper)

    def parseEntryList(self, response):
        papers = response.xpath("/html/body[@class='with-cu-identity']/div[@id='content']/div[@id='dlpage']/dl/dt/span[@class='list-identifier']/a[1]/@href").extract()
        for paper in papers:
            paper_url = urljoin('https://arxiv.org', paper)
            yield scrapy.Request(paper_url, callback=self.parsePaper)

    def parsePaper(self, response):
        #print(response.xpath("/html/body[@class='with-cu-identity']/div[@class='flex-wrap-footer']/main/div[@id='content']/div[@id='abs-outer']/div[@class='leftcolumn']/div[@id='content-inner']/div[@id='abs']/h1[@class='title mathjax']/text()"))
        item = ArxivPaperItem()

        item['arxiv_id'] = ""

        # tittle
        item['title'] = response.xpath("/html/body[@class='with-cu-identity']/div[@class='flex-wrap-footer']/main/div[@id='content']/div[@id='abs-outer']/div[@class='leftcolumn']/div[@id='content-inner']/div[@id='abs']/h1[@class='title mathjax']/text()").extract()[0]

        # year date
        datelist = response.xpath("/html/body[@class='with-cu-identity']/div[@class='flex-wrap-footer']/main/div[@id='content']/div[@id='abs-outer']/div[@class='leftcolumn']/div[@id='content-inner']/div[@id='abs']/div[@class='dateline']/text()").extract()
        tmp_date = "".join(datelist)
        #  [Submitted on 2 Nov 1992 (), last revised 25 Nov 1992 (this version, v2)]
        if "last" in tmp_date:
            year_e = tmp_date.find(" (this version")
            # [Submitted on 14 Dec 1998 (v1), last revised 26 Jul 1999
            tmp_str = tmp_date[:year_e]
            item['year'] = tmp_str[-4:]
            if tmp_str[-12] == " ":
                item['date'] = tmp_str[-11:-5]
            elif tmp_str[-11] == " ":
                item['date'] = tmp_str[-10:-5]
            else:
                logger.error('Exception happened when extract date, pdf is %s' % (item['title']))
        # [Submitted on 7 Dec 1992]
        else:
            item['year'] = tmp_date[-5:-1]
            date_b = tmp_date.find("on ")
            item['date'] = tmp_date[date_b + 3:-6]

        # type
        item['type'] = 'journal'

        # abstract
        tmp_abstract = ''.join(response.xpath("/html/body[@class='with-cu-identity']/div[@class='flex-wrap-footer']/main/div[@id='content']/div[@id='abs-outer']/div[@class='leftcolumn']/div[@id='content-inner']/div[@id='abs']/blockquote[@class='abstract mathjax']/text()").extract()).strip().replace('\n',' ')
        item['abstract'] = tmp_abstract
        # if len(tmp_abstract) > 0:
        #     item['abstract'] = str(tmp_abstract[0])
        # else:
        #     item['abstract'] = ""

        # pdf  arxiv_id
        try:
            # https://arxiv.org/pdf/hep-ph/9209298
            tmp_pdf = response.xpath("/html/body[@class='with-cu-identity']/div[@class='flex-wrap-footer']/main/div[@id='content']/div[@id='abs-outer']/div[@class='extra-services']/div[@class='full-text']/ul/li[1]/a[@class='abs-button download-pdf']/@href").extract()[0]
            item['pdf'] = 'https://arxiv.org' + tmp_pdf
            pdf_url_b = tmp_pdf.find("/pdf")
            item['arxiv_id'] = tmp_pdf[pdf_url_b+5:]
        except Exception as e:
            logger.error('Exception %s happened when extract pdf, pdf is %s' % (e, item['title']))  # TODO “Efficiently handling constraints with Metropolis-adjusted Langevin algorithm” withdrawn

        # volume
        item['volume'] = 'abs/' + item['arxiv_id']

        # citeThis 暂不用
        # TODO
        item['citeThis'] = []

        # pages
        # TODO
        item['pages'] = ""

        # doi
        # !!浏览器会对html文本进行规范化，自动在路径中加入tbody，导致读取失败，在路径中去除tbody即可
        # 不同页面tr数不同
        try:
            item["doi"] = response.xpath("/html/body[@class='with-cu-identity']/div[@class='flex-wrap-footer']/main/div[@id='content']/div[@id='abs-outer']/div[@class='leftcolumn']/div[@id='content-inner']/div[@id='abs']/div[@class='metatable']/table/tr/td[@class='tablecell arxivdoi']/a//text()").extract()[0]
        except Exception as e:
            item["doi"] = ""
            logger.warning('Exception %s happened when extract doi, pdf is "%s"' % (e, item['title']))

        # venue
        item['venue'] = 'ArXiv'

        # authors
        tmp_authors = response.xpath("/html/body[@class='with-cu-identity']/div[@class='flex-wrap-footer']/main/div[@id='content']/div[@id='abs-outer']/div[@class='leftcolumn']/div[@id='content-inner']/div[@id='abs']/div[@class='authors']/a/text()").extract()  # 原始版本xpath有问题
        if len(tmp_authors) > 0:
            item['authors'] = tmp_authors
        else:
            item['authors'] = list()

        # venue_id 暂不用
        # TODO
        item['venue_id'] = None

        # pdf_content_id 暂不用
        # TODO
        item['pdf_content_id'] = None

        # video_id 该阶段不用
        # TODO
        item['video_id'] = ""

        # blog_id 该阶段不用
        # TODO
        item['blog_id'] = ""

        # inCitationsCount
        # TODO
        item['inCitationsCount'] = 0

        # outCitationsCount
        # TODO
        item['outCitationsCount'] = 0

        # video_path 暂不用
        # TODO
        item['video_path'] = [""]

        # dblp_mdate
        item['dblp_mdate'] = ''

        # dblp_id
        item['dblp_id'] = ''

        # clean
        item['clean'] = ''

        yield item










