import scrapy
from scicrawl.items import ACLPaperItem
import yaml
from urllib.parse import urljoin
import logging
import os
from bson import ObjectId
from utils.logger import logger

# logging_config_file = './logging_config.yaml'

# # 设置日志
# with open(logging_config_file, 'r') as f:
#     config = yaml.safe_load(f.read())
#     config['handlers']['file']['filename'] += "_aclspider.log"
#     config['handlers']['info_file_handler']['filename'] += "_aclspider.log"
#     print(config)
#     logging.config.dictConfig(config)
#     f.close()
# logger = logging.getLogger(__name__)


class ACLSpider(scrapy.Spider):
    name = 'aclspider'
    allowed_domains = ['aclanthology.org']

    # ACL中不同的venue
    venues = ['aacl', 'acl', 'aespen', 'aha', 'ai4hi', 'akbc', 'alnlp', 'alr', 'alta', 'alvr', 'alw', 'amta', 'anlp',
              'argmining', 'atanlp', 'atsma', 'autosimtrans', 'bea', 'bioasq', 'bionlp', 'birndl', 'blackboxnlp',
              'bsnlp', 'bucc', 'calcs', 'catocl', 'ccnlg', 'ccurl', 'challengehml', 'cl', 'cl4lc', 'clfl',
              'clinicalnlp', 'cllrd', 'clp', 'clpsych', 'clssts', 'cltw', 'cmcl', 'cmlc', 'cns', 'codeswitch', 'codi',
              'cogacll', 'cogalex', 'coling', 'comacoma', 'computerm', 'conll', 'corbon', 'cosli', 'crac', 'csct',
              'cvir', 'cvsc', 'deelio', 'depling', 'discomt', 'dmr', 'dmtw', 'eacl', 'eamt', 'ecnlp', 'ecomnlp',
              'emnlp', 'enlg', 'ethnlp', 'eval4nlp', 'events', 'eventstory', 'exprom', 'fever', 'figlang', 'findings',
              'finnlp', 'fnp', 'framenet', 'fsmnlp', 'gamnlp', 'geaf', 'gebnlp', 'gems', 'gendeep', 'gl', 'globalex',
              'gramlex', 'gwc', 'hlt', 'hytra', 'icon', 'icos', 'ijcnlp', 'inlg', 'insights', 'intexsempar', 'isa',
              'iwclul', 'iwcs', 'iwdp', 'iwltp', 'iwpt', 'iwslt', 'knlp', 'lantern', 'lasm', 'latech', 'latechclfl',
              'latentvar', 'law', 'lccm', 'ldl', 'lglp', 'lifelongnlp', 'lilt', 'lincr', 'loresmt', 'louhi', 'lr4nlp',
              'lr4sshoc', 'lrec', 'lsdsem', 'lt4dh', 'lt4gov', 'lt4hala', 'lt4var', 'metaphor', 'mmw', 'mol', 'moocs',
              'msr', 'mtsummit', 'muc', 'multiling', 'multilingualbio', 'mwe', 'mwelex', 'naacl', 'nespnlp', 'news',
              'ngt', 'nli', 'nlp4call', 'nlp4convai', 'nlp4if', 'nlp4ita', 'nlp4musa', 'nlp4tm', 'nlpbt', 'nlpcovid19',
              'nlpcss', 'nlplod', 'nlpmc', 'nlposs', 'nlptea', 'nmt', 'nodalida', 'nsurl', 'nuse', 'oiaf4hlt', 'onion',
              'osact', 'paclic', 'pam', 'parlaclarin', 'peoples', 'pitr', 'prep', 'privatenlp', 'pylo', 'rail', 'ranlp',
              'rdsm', 'readi', 'repeval', 'repl4nlp', 'restup', 'robonlp', 's2mt', 'sadaatl', 'scai', 'scil', 'sclem',
              'sdp', 'sedmt', 'sembear', 'semdeep', 'semeval', 'semitic', 'sense', 'sew', 'sigdial', 'sighan',
              'sigmorphon', 'signlang', 'sigtyp', 'slpat', 'sltu', 'smm4h', 'socialnlp', 'splu', 'spmrl', 'spnlp',
              'ssst', 'starsem', 'statfsm', 'step', 'stil', 'stoc', 'storynlp', 'stylevar', 'sustainlp', 'swaie',
              'tacl', 'tag', 'teachingnlp', 'textgraphs', 'textinfer', 'tinlap', 'tipster', 'tlt', 'trac', 'ttnls',
              'udw', 'vardial', 'vl', 'vlc', 'wac', 'wamm', 'wanlp', 'wassa', 'wat', 'webnlg', 'wildre', 'winlp', 'wmt',
              'wnut', 'wosp', 'ws', 'wssanlp']
    base_url = "https://aclanthology.org/venues/"
    venue = 0
    venue_url = base_url + venues[0]  # 当前正在处理venue的url
    start_urls = [venue_url]

    acl_venues = ['AACL', 'ACL', 'ANLP', 'CL', 'CoNLL', 'EACL', 'EMNLP', 'NAACL', 'SemEval', '*SEM', 'TACL', 'WMT']
    non_acl_venues = ['ALTA', 'AMTA', 'COLING', 'EAMT', 'HLT', 'IJCNLP', 'LREC', 'MUC', 'PACLIC', 'RANLP', 'TINLAP',
                      'TIPSTER']

    def parse(self, response):
        logger.info('Crawling ' + self.venue_url)

        # 该venue中 所有年份内的所有volumes
        volumes = response.xpath('//*[@id="main"]/div/div/div/ul/li/a/@href').extract()
        for volume in volumes:
            volume_url = urljoin('https://aclanthology.org/', volume)
            yield scrapy.Request(volume_url, callback=self.parseVolumn)

        logger.info('Finished ' + self.venue_url)

        if self.venue < len(self.venues) - 1:
            # 处理下一个venue
            self.venue += 1
            self.venue_url = self.base_url + self.venues[self.venue]
            yield scrapy.Request(self.venue_url, callback=self.parse)

    def parseVolumn(self, response):
        papers = response.xpath('//*[@id="main"]/div[2]/p/span[2]/strong/a/@href').extract()

        for paper in papers:
            paper_url = urljoin('https://aclanthology.org/', paper)
            yield scrapy.Request(paper_url, callback=self.parsePaper)

    def parsePaper(self, response):
        item = ACLPaperItem()
        # 新数据库中没有
        # anthology_id
        item['anthology_id'] = response.xpath('//*[@id="main"]/div/div[1]/dl/dd[1]/text()').extract()[0]

        # volume
        tmp_volume = response.xpath('//*[@id="main"]/div/div[1]/dl/dd[2]/a/text()').extract()
        if len(tmp_volume) > 0:
            item['volume'] = str(tmp_volume[0])
        else:
            item['volume'] = ""

        # type
        # TODO
        item['type'] = ''

        # date
        tmp_date = response.xpath('//*[@id="main"]/div/div[1]/dl/dd[3]/text()').extract()
        if len(tmp_date) > 0:
            item['date'] = str(tmp_date[0])
        else:
            item['date'] = ""

        # year 
        tmp_year = response.xpath('//*[@id="main"]/div/div[1]/dl/dd[4]/text()').extract()
        if len(tmp_year) > 0:
            item['year'] = str(tmp_year[0])
        else:
            item['year'] = ""

        # citeThis 暂不用
        # TODO
        item['citeThis'] = []

        # venue
        # 需要筛选
        tmp_venue = response.xpath(
            '//*[@id="main"]/div/div[1]/dl/dd[6]/a/text()').extract()  # 可能有多个, 例如https://www.aclweb.org/anthology/2020.law-1.1/
        if len(tmp_venue) > 0:
            item['venue'] = tmp_venue

            for venue in item['venue']:
                if venue in self.acl_venues:
                    item['venue'] = venue
                    break
                elif venue in self.non_acl_venues:
                    item['venue'] = venue
                    break
                else:
                    continue
        else:
            item['venue'] = ''

        if isinstance(item['venue'], list):
            item['venue'] = ''

        # pages
        tmp_pages = response.xpath('//*[@id="main"]/div/div[1]/dl/dd[10]/text()').extract()
        if len(tmp_pages) > 0:
            item['pages'] = str(tmp_pages[0])
        else:
            item['pages'] = ""

        # 新表中没有该字段
        # url
        # tmp_url = response.xpath('//*[@id="main"]/div/div[1]/dl/dd[12]/a/@href').extract()
        # if len(tmp_url) > 0:
        #     item['url'] = str(tmp_url[0])
        # else:
        #     item['url'] = ""

        # doi
        tmp_doi = response.xpath('//*[@id="main"]/div/div[1]/dl/dd[13]/a/text()').extract()
        if len(tmp_doi) > 0:
            item['doi'] = 'https://doi.org/' + str(tmp_doi[0])
        else:
            item['doi'] = ""

        # title
        papernames = response.xpath('//*[@id="title"]/a')
        name = ""
        for _, papername in enumerate(papernames):
            name += str(papername.xpath('//text()').extract()[0])
        item['title'] = name[:-16]

        # authors
        tmp_authors = response.xpath('//*[@id="main"]/div/p/a/text()').extract()  # 原始版本xpath有问题
        if len(tmp_authors) > 0:
            item['authors'] = tmp_authors
        else:
            item['authors'] = list()

        # abstract
        tmp_abstract = response.xpath('//*[@id="main"]/div/div[1]/div/div/text()').extract()
        if len(tmp_abstract) > 0:
            item['abstract'] = str(tmp_abstract[0])
        else:
            item['abstract'] = ""

        contents = response.xpath('//*[@id="main"]/div/div[1]/dl/dt/text()').extract()

        for i in range(len(contents)):
            if contents[i] == 'Bib Export formats:' or contents[i] == 'Copy Citation:':
                start = i + 2
                break

        attachment_types = ['software', 'dataset', 'poster']
        for i in range(start, len(contents) + 1):
            _xpath = '//*[@id="main"]/div/div[1]/dl/dd[%d]/a/@href' % i
            _xpath_fname = '//*[@id="main"]/div/div[1]/dl/dd[%d]/a/text()' % i

            attachment_type = contents[i - 1][:-1]  # 去掉冒号
            attachment = response.xpath(_xpath).extract()[0]

            if attachment_type == 'PDF':
                item['pdf'] = attachment
                # 新数据库中没有
                # 检查pdf_path
                # item['pdf_path'] = self.checkPath(item['anthology_id'], type = 'pdf')
                # item['pdf_content_id'] = ObjectId('601f51e9809e2c9c7dba7584')

            elif attachment_type == 'Video':
                item['video_url'] = attachment
                # 检查video_path
                item['video_path'] = self.checkPath(item['anthology_id'], type='video')

                if 'slideslive' in item['video_url']:
                    # 可能会有切分成图片的slide
                    if 'slide_url' not in item:
                        item['slide_url'] = item['video_url']
                        item['slide_path'] = self.checkPath(item['anthology_id'], filename=item['anthology_id'])

            # 新数据库中没有
            # elif attachment_type.lower() == 'presentation':
            #     if attachment != 'https://www.aclanthology.org/anthology/attachments':
            #         item['slide_url'] = attachment
            #         attachment_fname = response.xpath(_xpath_fname).extract()[0][1:]
            #         item['slide_path'] = self.checkPath(item['anthology_id'], filename = attachment_fname)
            #
            # elif attachment_type.lower() in attachment_types:
            #     if attachment != 'https://www.aclanthology.org/anthology/attachments':
            #         item[attachment_type.lower() + '_url'] = attachment
            #         attachment_fname = response.xpath(_xpath_fname).extract()[0][1:]
            #         item[attachment_type.lower() + '_path'] = self.checkPath(item['anthology_id'], filename = attachment_fname)

        if 'pdf' not in item:
            item['pdf'] = ''
            # item['pdf_path'] = ''
        if 'video_url' not in item:
            item['video_url'] = ''
            item['video_path'] = ''

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

        # 新表中没有该字段
        # item['other_attachments'] = list()
        item['dblp_id'] = ''
        item['dblp_mdate'] = ''
        item['clean'] = ''

        yield item

    def checkPath(self, anthology_id, type='', filename=''):

        if type == 'pdf':
            filename = anthology_id + '.pdf'
        elif type == 'video':
            filename = anthology_id + '.mp4'

        ori_path = '/home/xcx/data/HammerScholar/aclanthology/' + anthology_id + '/' + filename
        path = ''
        if os.path.exists(ori_path):
            path = '/hammerscholar/aclanthology/' + anthology_id + '/' + filename

        return path