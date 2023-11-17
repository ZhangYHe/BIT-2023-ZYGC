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

        elif isinstance(item, SciHubPaperItem): # 更新mongodb数据库中 doi对应的file name
            # 查询是否已存在相同的 DOI 记录
            existing_record = self.clean_papers_tb.find_one({"*doi": item["doi"]})

            if existing_record:
                # 如果已存在，则更新文件名
                self.clean_papers_tb.update_one({"*doi": item["doi"]}, {"$set": {"filename": item['file_name']}})
                logger.info(f"Update DOI: {item['doi']}，文件名: {item['file_name']}")
            else:
                # 如果不存在，则插入新记录
                self.clean_papers_tb.insert_one({"*doi": item["doi"], "filename": item['file_name']})
                logger.info(f"Insert new record ，DOI: {item['doi']}，文件名: {item['file_name']}")


        elif isinstance(item, ACMPaperItem):  # TODO
            logger.error("IN PIPLINES ACM")

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
            query = {'title': title, 'year': year}
            del item['venue']
            self.clean_papers_tb.update_many(query, {'$set':item})


    def close_spider(self,spider):
        logger.info('Total insert %d papers' % self.insert_total)
        logger.info('Total update %d papers' % self.update_total)
        self.f.close()
        self.client.close()


class MyFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # 1
        '''自定义保存路径,以的url保存,重写前是url经过MD5编码后存储'''
        # file_path = "".join(re.findall("https://matplotlib.org/([\w\W]+)", request.url)) #TODO
        # return f'file_dir/{file_path}'

        # 2
        # filename = request.meta['name']  # 获取视频文件名
        # return filename  # 返回下载的视频文件名

        # 3
        # image_url_hash = hashlib.shake_256(request.url.encode()).hexdigest(5)
        # image_perspective = request.url.split("/")[-2]
        # image_filename = f"{image_url_hash}_{image_perspective}.jpg"
        #
        # return image_filename

        # 4 原始文件名
        # https://example.com/a/b/c/foo.pngfilesfiles/foo.png
        #return "files/" + PurePosixPath(urlparse(request.url).path).name

        # 5
        # 设置保存的文件名
        find_name = re.compile(r"/(.*?)?download=true")
        file_name = re.findall(find_name, request.url)[0]
        file_name = file_name.split('/')[-1]
        file_name = file_name[0:len(file_name) - 1]
        item["file_name"] = file_name
        logger.info('Downloading %s ' % item["file_name"])
        return file_name

    def item_completed(self, results, item, info): #TODO 是否要加？ 官方文档
        return item

    # 此方法FilesPipeline和ImagesPipeline内部已经执行, 可以省略不重写 TODO 可以重写添加请求头
    # def get_media_requests(self, item, info):
    #     for file_url in item['file_urls']:
    #         yield Request(file_url)

    # 此方法FilesPipeline和ImagesPipeline内部已经执行, 可以省略不重写 TODO 可以重写添加请求头
    # def item_completed(self, results, item, info):
    #     file_paths = [x['path'] for ok, x in results if ok]
    #     if not file_paths:
    #         raise DropItem("Item contains no files")
    #     item['file_paths'] = file_paths
    #     return item
