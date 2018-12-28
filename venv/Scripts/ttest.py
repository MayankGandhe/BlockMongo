import datetime
import hashlib
import json
import pymongo

class DataBase:
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient.list_database_names()
    def __init__(self,db_name = "blockchain"):
        dblist = self.myclient.list_database_names()
        if db_name  in dblist:

           self.mydb = self.myclient[db_name]
           print("Connected")



    def insert_db(self,block):
        chain = self.mydb["chain"]
        chain.insert_one(block)

    def retrive_data(self):
        y = []
        for x in self.mydb["chain"].find():
           print(x)
           y.append(x)
        return y


class BlockChain:
    database = DataBase("blockchain")
    def __init__(self):
        self.chain = []

    def retrive_block(self):
        self.chain = self.database.retrive_data()

    def create_block(self,data):
        nonce = 0
        self.retrive_block()
        if len(self.chain) >= 1:
            block = dict(_id=(len(self.chain)) + 1,timestam = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), data=data, pre_hash=hashlib.sha256(str(self.get_block(len(self.chain))).encode()).hexdigest(), nonce=0)
        else:
            block = dict(_id=(len(self.chain)) + 1,timestam = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), data=data, pre_hash="0", nonce=0)
            # self.database.insert_db(block)

        proof_hash = hashlib.sha256(str(block).encode()).hexdigest()
        while proof_hash[:4] != "0000":
            nonce +=1
            block["nonce"] = nonce
            proof_hash = hashlib.sha256(str(block).encode()).hexdigest()

        print(block)
        self.chain.append(block)
        self.database.insert_db(block)
        return block

    def get_block(self,index):
        return (self.chain[index-1])

    def verify_block(self):
        last_point = len(self.chain)
        flag =0
        block = self.chain[1]
        current_point = 2
        pre_block = self.chain[0]
        flag = 1
        count = 0
        print(last_point)
        while block["_id"] != last_point + 1:
            # count +=1
            if block["pre_hash"] == hashlib.sha256(str(pre_block).encode()).hexdigest():
                if block["_id"] == last_point:
                    break

                pre_block = block
                block = self.chain[current_point]
                current_point += 1
                print(block["_id"])
            else:
                print("Not Valid")

                flag = 0
                break
        if flag == 1:
            print("Valid")





blockchain = BlockChain()
blockchain.create_block("hello")
blockchain.create_block("teest")
tet = blockchain.create_block("teest")
blockchain.create_block("teest")
print(blockchain.chain)
f = open("db.json", "w")
f.write(str(blockchain.chain))
f = open("db.json", "r")
json_string = f.read()
json_obj = json.dumps(json_string)
blockchain.verify_block()





