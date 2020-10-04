from bson.objectid import ObjectId
from pymongo import UpdateOne, ReplaceOne
from pymongo.errors import BulkWriteError

from flask_restful import Resource, fields, marshal_with, marshal
from flask import render_template, make_response, request

from zipline.db import DatabaseCollection
from zipline.helpers import modify_product, modify_products, resource_field_update, resource_fields_product, resource_field_bulk_write


db = DatabaseCollection()
collection = db.get_collection()

class Home(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'),200,headers)


class ProductListView(Resource):
    """
    TODO: Add Swagger
    TODO: Add Docmentation
    TODO: Add Logger
    TODO: Home Page Doc
    """

    def get(self):
        results = []
        limit = request.args.get('limit', default=5, type=int)
        skip = request.args.get('skip', default=0, type=int)
        for d in collection.find().skip(skip).limit(limit):
            results.append(modify_product(d))
        return {"products": results, "skip": skip, "limit": limit}
        
    def post(self):
        results = []
        ids = collection.insert_many(request.json).inserted_ids
        for i in ids:
            results.append({"ObjectId": str(i)})
        return results
    
    @marshal_with(resource_field_bulk_write)
    def patch(self):
        requests = []
        for q in request.json:
            print(q)
            requests.append(UpdateOne({"_id": ObjectId(q["_id"])},{"$set": q["data"]}))
        try:
            obj = collection.bulk_write(requests, ordered=False)
        except BulkWriteError as bwe:
            print(bwe)
            # logger
        return obj

    @marshal_with(resource_field_bulk_write)
    def put(self):
        requests = []
        for q in request.json:
            requests.append(ReplaceOne({"_id": ObjectId(q["_id"])}, q["data"]))
        try:
            obj = collection.bulk_write(requests, ordered=False)
        except BulkWriteError as bwe:
            print(bwe)
            # logger
        return obj


class ProductInstanceView(Resource):
    """
     
    """
    def get(self, product_id):
        obj = collection.find_one({"_id": ObjectId(product_id)})
        if obj:
            return {"product": modify_product(obj)}
        else:
            return {"message": "Object not present"}, 404
    
    @marshal_with(resource_field_update)
    def patch(self, product_id):
        obj = collection.update_one({"_id": ObjectId(product_id)}, {"$set" : request.json })
        return obj

    @marshal_with(resource_field_update)
    def put(self, product_id):
        obj = collection.replace_one({"_id": ObjectId(product_id)}, request.json )
        return obj

    def post(self):
        id_ = collection.insert_one(request.json).inserted_id
        return {"ObjectId": str(id_)}
