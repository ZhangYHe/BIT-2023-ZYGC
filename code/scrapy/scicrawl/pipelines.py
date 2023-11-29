# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import pymongo
from utils.logger import logger
from scicrawl.items import *
from scrapy.pipelines.files import FilesPipeline
import re

class ScicrawlPipeline:
    def open_spider(self,spider):
        self.f = open('./papers.json','w',encoding='utf-8')

        # vultr服务器测试
        self.client = pymongo.MongoClient("mongodb://admin:202309@64.176.214.218:27017/?authMechanism=DEFAULT")
        db = self.client['Scholar']
        self.clean_papers_tb = db['clean_papers']
        self.authors_tb = db['authors']


        self.insert_total = 0
        self.update_total = 0


    def process_item(self, item, spider):
        self.f.write(json.dumps(dict(item), ensure_ascii=False))
        self.f.write('\n')
        #item['authors'] = [self.matchAuthor(author) for author in item['authors']]  #移动到下面if else中
        star_item = ['title', 'year', 'volume', 'type', 'abstract', 'pdf', 'citeThis', 'pages', 'doi', 'venue',
                     'date', 'authors', 'venue_id', 'pdf_content_id', 'video_id', 'blog_id', 'inCitationsCount',
                     'outCitationsCount', 'video_path']

        if isinstance(item,ACLPaperItem):
            item['authors'] = [self.matchAuthor(author) for author in item['authors']]
            #logger.error('acl_spider')
            count = self.clean_papers_tb.count_documents({'anthology_id': item['anthology_id']})

            # 为字段名前添加*
            insert_dict = {}
            for key, val in item.items():
                # 需要添加*
                if key in star_item:
                    insert_dict['*' + key] = val
                else:
                    insert_dict[key] = val

            if count == 0:
                # 原版字段前无*，直接insert即可
                # self.clean_papers_tb.insert_one(item)
                self.clean_papers_tb.insert_one(insert_dict)
                self.insert_total += 1
            elif count > 0:
                # return_state = self.clean_papers_tb.update_many({'anthology_id': item['anthology_id']}, {'$set':item}) # cursor
                # 插入处理后的字典
                return_state = self.clean_papers_tb.update_many({'anthology_id': item['anthology_id']}, {'$set': insert_dict})  # cursor
                self.update_total += return_state.modified_count
                # self.update_item(item, papers)

            return item

        elif isinstance(item, ArxivPaperItem):
            item['authors'] = [self.matchAuthor(author) for author in item['authors']]
            #logger.error('arxiv_spider')
            count = self.clean_papers_tb.count_documents({'arxiv_id': item['arxiv_id']})         #测试

            # 为字段名前添加*
            insert_dict = {}
            for key, val in item.items():
                # 需要添加*
                if key in star_item:
                    insert_dict['*' + key] = val
                else:
                    insert_dict[key] = val

            if count == 0:
                # 原版字段前无*，直接insert即可
                # self.clean_papers_tb.insert_one(item)
                self.clean_papers_tb.insert_one(insert_dict)
                self.insert_total += 1
                #logger.info("arxiv_spider insert one item")
            elif count > 0:
                return_state = self.clean_papers_tb.update_many({'arxiv_id': item['arxiv_id']},{'$set': insert_dict})  # 测试
                self.update_total += return_state.modified_count
                # self.update_item(item, papers)

            return item


    def update_item(self, item, papers):
        for paper in papers:
            new_fields = {}
            for key, val in item.items():
                if key not in paper:
                    new_fields[key] = val
            if new_fields != {}:
                self.clean_papers_tb.update_one({'_id': paper['_id']}, {'$set': new_fields})

    def matchAuthor(self, author):
        try:
            author_data = self.authors_tb.find_one({'name': author})
            if author_data:
                return {'index': author_data.get('name_index',''), 'name': author, 'id': author_data['_id']}
            else:
                return_state = self.authors_tb.insert_one({
                    'name': author,
                    'last_name': author.split(' ')[-1],
                    'first_name': ' '.join(author.split(' ')[: -1]),
                    'name_index': '',
                    'ambiguous': False,
                    'other_names': [],
                    'dblp_key': "",
                    'orcid': "",
                    'orcid_certrain': False,
                    'profiles': {},
                    'affiliation': "",
                    'other_affiliation': []
                })

                return {'index': '', 'name': author, 'id': return_state.inserted_id}
        except Exception as e:
            logger.info('Exception %s happened when author is %s' % (e, author))

    def insert_item(self, item):
        title = item['title']
        year = item['year']
        venue = item['venue']

        if venue != '':
            query = {'title': title, 'year': year, 'venue': venue}

            self.clean_papers_tb.update_many(query, {'$set':item})

        else:
            query = {'title': title, 'year': year}PP
            del item['venue']
            self.clean_papers_tb.update_many(query, {'$set':item})


    def close_spider(self,spider):
        logger.info('Total insert %d papers' % self.insert_total)
        logger.info('Total update %d papers' % self.update_total)
        self.f.close()
        self.client.close()

