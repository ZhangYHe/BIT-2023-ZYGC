from pymongo import MongoClient
from bson import ObjectId

# 连接 MongoDB
client = MongoClient('mongodb://admin:202309@64.176.214.218:27017/?authMechanism=DEFAULT')
db = client['Scholar']

# 获取 authors 表和 clean_papers 表的引用
authors_collection = db['authors']
clean_papers_collection = db['clean_papers']
visualize_collection = db['visualize']

# 定义时间范围
start_year = 1990
end_year = 2025

# 遍历 authors 表
for author in authors_collection.find():
    author_id = author['_id']

    # 初始化 publication_periods 列表
    publication_periods = []

    # 处理1990年以前的数据
    tmp_paper_ids = []
    tmp_paper_count = 0
    for paper in clean_papers_collection.find({'*authors.id': author_id}):
        if not paper['*year']:
            continue
        paper_year = int(paper['*year'])
        if paper_year < start_year:
            tmp_paper_count += 1
            tmp_paper_ids.append(paper['_id'])

    print(f"Author: {author['name']}, Author ID: {author_id}")
    print(f"Paper count for years before {start_year}: {tmp_paper_count}")

    publication_periods.append({
        'start_year': None,  # 表示1990年以前
        'end_year': start_year - 1,
        'paper_count': tmp_paper_count,
        'paper_ids': tmp_paper_ids
    })


    for year in range(start_year, end_year, 5):
        paper_ids = []
        paper_count = 0
        for paper in clean_papers_collection.find({'*authors.id': author_id}):
            if not paper['*year']:
                continue

            try:
                paper_year = int(paper['*year'])
            except Exception as e:
                print("Error: ", e)
                continue

            if year <= paper_year < (year + 5):
                paper_count += 1
                paper_ids.append(paper['_id'])

        publication_periods.append({
            'start_year': year,
            'end_year': year + 4,
            'paper_count': paper_count,
            'paper_ids': paper_ids
        })

        # 检查是否已存在具有相同 author_id 的记录
        existing_record = visualize_collection.find_one({'author_id': author_id})

        if existing_record:
            # 如果记录已存在，使用 update_one 方法更新它
            visualize_collection.update_one(
                {'author_id': author_id},
                {'$set': {'publication_periods': publication_periods}}
            )
            print("update")
        else:
            # 如果记录不存在，创建 visualize 记录并插入
            visualize_record = {
                'name': author['name'],
                'author_id': author_id,
                'publication_periods': publication_periods
            }
            visualize_collection.insert_one(visualize_record)
            print("insert")

        print(f"Paper count for years before {year+5}: {paper_count}")

# 关闭 MongoDB 连接
client.close()
