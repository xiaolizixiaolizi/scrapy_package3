import  pymongo
from  pymongo.collection import Collection

class Connect_mongo(object):
    def __init__(self):
        self.client=pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db_data=self.client['dougou']

    def insert_item(self,item):
        db_collenction=Collection(self.db_data,'dougou_collection')
        db_collenction.insert(item)



mongo_info=Connect_mongo()