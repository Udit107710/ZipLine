from bson.objectid import ObjectId
from pymongo import UpdateOne, ReplaceOne, InsertOne, DeleteOne

from flask_restful import Resource, fields, marshal_with, marshal
from flask import render_template, make_response, request

from zipline.db import DatabaseCollection
from zipline.helpers import modify_product, modify_products, resource_field_update, resource_fields_product, resource_field_bulk_write, perform_bulk


db = DatabaseCollection()
collection = db.get_collection()

class Home(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'),200,headers)


class ProductListView(Resource):
    """
    Collection of APIs used for handling Products List as a resource
    """

    def get(self):
        """
        Get a list of products with pagnination support
        ---
        parameters:
            -   in: query
                name: limit
                schema:
                    type: integer
                description: The number of product objects to return
                required: false
            -   in: query
                name: skip
                schema:
                    type: integer
                description: The number of objects to skip fecthing
                required: false
        responses:
            '200':
                description: List of product objects with skip and limit used for querying db
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                products:
                                    description: List of products
                                    type: array
                                    items:
                                        schema:
                                            id: Product
                                            properties:
                                                _id:
                                                    type: ObjectId
                                                name:
                                                    type: string
                                                brand_name:
                                                    type: string
                                                regular_price_value:
                                                    type: number
                                                    format: float
                                                offer_price_value:
                                                    type: number
                                                    format: float
                                                currency:
                                                    type: string
                                                classification_l1:
                                                    type: string
                                                classification_l2:
                                                    type: string
                                                classification_l3:
                                                    type: string
                                                classification_l4:
                                                    type: string
                                                image_url:
                                                    type: string
                                skip:
                                    description: No. of products skipped from start, while fetching from db
                                    type: integer
                                limit:
                                    description: No. of items fetched
                                    type: integer
        """
        results = []
        limit = request.args.get('limit', default=5, type=int)
        skip = request.args.get('skip', default=0, type=int)
        for d in collection.find().skip(skip).limit(limit):
            results.append(modify_product(d))
        return {"products": results, "skip": skip, "limit": limit}

    @marshal_with(resource_field_bulk_write)
    def post(self):
        """
        Create Product objects
        ---
        parameters:
            -   in: body
                description: List of Product objects to be inserted to database
                required: true
                schema:
                    type: array
                    items:
                        properties:
                            name:
                                type: string
                            brand_name:
                                type: string
                            regular_price_value:
                                type: number
                                format: float
                            offer_price_value:
                                type: number
                                format: float
                            currency:
                                type: string
                            classification_l1:
                                type: string
                            classification_l2:
                                type: string
                            classification_l3:
                                type: string
                            classification_l4:
                                type: string
                            image_url:
                                type: string
        responses:
            '200':
                description: Bulk Write result object from MongoDB
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                acknowledged:
                                    type: boolean
                                matched_count:
                                    type: string
                                modified_count:
                                    type: integer
                                deleted_count:
                                    type: integer
                                upserted_ids:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            _id:
                                                type: string
                                inserted_count:
                                    type: integer
            '500':
                description: Server encountered an error while performing bulk operation
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                message:
                                    type: string
        """
        requests = []
        for q in request.json:
            requests.append(InsertOne(q))
        return perform_bulk(collection, requests), 201

    @marshal_with(resource_field_bulk_write)
    def patch(self):
        """
        Modify details of existing Product objects
        ---
        parameters:
            -   in: body
                description: List of Product objects to be inserted to database
                required: true
                schema:
                    type: array
                    items:
                        properties:
                            _id:
                                type: string
                            data:
                                type: object
                                properties:
                                    name:
                                        type: string
                                    brand_name:
                                        type: string
                                    regular_price_value:
                                        type: number
                                        format: float
                                    offer_price_value:
                                        type: number
                                        format: float
                                    currency:
                                        type: string
                                    classification_l1:
                                        type: string
                                    classification_l2:
                                        type: string
                                    classification_l3:
                                        type: string
                                    classification_l4:
                                        type: string
                                    image_url:
                                        type: string
        responses:
            '200':
                description: Bulk Write result object from MongoDB
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                acknowledged:
                                    type: boolean
                                matched_count:
                                    type: string
                                modified_count:
                                    type: integer
                                deleted_count:
                                    type: integer
                                upserted_ids:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            _id:
                                                type: string
                                inserted_count:
                                    type: integer
            '500':
                description: Server encountered an error while performing bulk operation
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                message:
                                    type: string
        """
        requests = []
        for q in request.json:
            requests.append(UpdateOne({"_id": ObjectId(q["_id"])},{"$set": q["data"]}))
        return perform_bulk(collection, requests)

    @marshal_with(resource_field_bulk_write)
    def put(self):
        """
        Replace existing Product objects
        ---
        parameters:
            -   in: body
                description: List of Product objects to be inserted to database
                required: true
                schema:
                    type: array
                    items:
                        properties:
                            _id:
                                type: string
                            data:
                                type: object
                                properties:
                                    name:
                                        type: string
                                    brand_name:
                                        type: string
                                    regular_price_value:
                                        type: number
                                        format: float
                                    offer_price_value:
                                        type: number
                                        format: float
                                    currency:
                                        type: string
                                    classification_l1:
                                        type: string
                                    classification_l2:
                                        type: string
                                    classification_l3:
                                        type: string
                                    classification_l4:
                                        type: string
                                    image_url:
                                        type: string
        responses:
            '200':
                description: Bulk Write result object from MongoDB
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                acknowledged:
                                    type: boolean
                                matched_count:
                                    type: string
                                modified_count:
                                    type: integer
                                deleted_count:
                                    type: integer
                                upserted_ids:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            _id:
                                                type: string
                                inserted_count:
                                    type: integer
            '500':
                description: Server encountered an error while performing bulk operation
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                message:
                                    type: string
        """
        requests = []
        for q in request.json:
            requests.append(ReplaceOne({"_id": ObjectId(q["_id"])}, q["data"]))
        return perform_bulk(collection, requests), 201

    @marshal_with(resource_field_bulk_write)
    def delete(self):
        """
        Delete multiple object(s) based on a filter
        ---
        parameters:
            -   in: body
                description: List of filter fields and value, on basis of which the object(s) will be deleted
                schema:
                    type: array
                    items:
                        anyOf:
                            - schema:
                                properties:
                                    _id:
                                    type: string
                            - schema:
                                properties:
                                    name:
                                    type: string
                            - schema:
                                properties:
                                    brand_name:
                                    type: string
                            - schema:
                                properties:
                                    regular_price_value:
                                    type: number
                                    format: float
                            - schema:
                                properties:
                                    offer_price_value:
                                    type: number
                                    format: float
                            - schema:
                                properties:
                                    currency:
                                    type: string
                            - schema:
                                properties:
                                    classification_l1:
                                    type: string
                            - schema:
                                properties:
                                    classification_l2:
                                    type: string
                            - schema:
                                properties:
                                    classification_l3:
                                    type: string
                            - schema:
                                properties:
                                    classification_l4:
                                    type: string
                            - schema:
                                properties:
                                    image_url:
                                    type: string
        responses:
            '200':
                description: Bulk Write result object from MongoDB
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                acknowledged:
                                    type: boolean
                                matched_count:
                                    type: string
                                modified_count:
                                    type: integer
                                deleted_count:
                                    type: integer
                                upserted_ids:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            _id:
                                                type: string
                                inserted_count:
                                    type: integer
            '500':
                description: Server encountered an error while performing bulk operation
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                message:
                                    type: string
        """
        requests = []
        for q in request.json:
            requests.append(DeleteOne(q))
        return perform_bulk(collection, requests), 200

class ProductInstanceView(Resource):
    """
    This resource handles all the requests related to a single Product object
    """

    def get(self, product_id):
        """
        Fetch a single obejct with Id
        ---
        parameters:
            -   in: path
                name: product_id
                description: Id of the object trying to fetch from db
                schema:
                    type: string
                required: true
        responses:
            '200':
                description: Fetched the Product object successfully
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                product:
                                    type: object
                                    properties:
                                        _id:
                                            type: string
                                        name:
                                            type: string
                                        brand_name:
                                            type: string
                                        regular_price_value:
                                            type: number
                                            format: float
                                        offer_price_value:
                                            type: number
                                            format: float
                                        currency:
                                            type: string
                                        classification_l1:
                                            type: string
                                        classification_l2:
                                            type: string
                                        classification_l3:
                                            type: string
                                        classification_l4:
                                            type: string
                                        image_url:
                                            type: string
            '404':
                description: No Product object with the given Id found
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                message:
                                    type: string
            '500':
                description: Some error occured, check logs
        """
        obj = collection.find_one({"_id": ObjectId(product_id)})
        if obj:
            return {"product": modify_product(obj)}
        else:
            return {"message": "Object not present"}, 404
    
    @marshal_with(resource_field_update)
    def patch(self, product_id):
        """
        Alter values of a single object
        ---
        parameters:
            -   in: path
                name: product_id
                description: Id of the object which will have it's values altered
                schema:
                    type: string
                required: true
            -   in: body
                description: Data which needs to be changed
                schema:
                    type: object
                    properties:
                        anyOf:
                            name:
                                type: string
                            brand_name:
                                type: string
                            regular_price_value:
                                type: number
                                format: float
                            offer_price_value:
                                type: number
                                format: float
                            currency:
                                type: string
                            classification_l1:
                                type: string
                            classification_l2:
                                type: string
                            classification_l3:
                                type: string
                            classification_l4:
                                type: string
                            image_url:
                                type: string
        responses:
            '200':
                description: Object's values altered succesfully
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                acknowledged:
                                    type: boolean
                                matched_count:
                                    type: string
                                modified_count:
                                    type: integer
                                upserted_id:
                                    type: integer
            '500':
                description: Some error occured, check logs
        """
        obj = collection.update_one({"_id": ObjectId(product_id)}, {"$set" : request.json })
        return obj

    @marshal_with(resource_field_update)
    def put(self, product_id):
        """
        Replace existing objects
        ---
        parameters:
            -   in: path
                name: product_id
                description: Id of the object which will have it's values altered
                schema:
                    type: string
                required: true
            -   in: body
                description: New object to replace the existing object with
                schema:
                    type: object
                    properties:
                        name:
                            type: string
                        brand_name:
                            type: string
                        regular_price_value:
                            type: number
                            format: float
                        offer_price_value:
                            type: number
                            format: float
                        currency:
                            type: string
                        classification_l1:
                            type: string
                        classification_l2:
                            type: string
                        classification_l3:
                            type: string
                        classification_l4:
                            type: string
                        image_url:
                            type: string
        responses:
            '200':
                description: Object replaced sucessfully
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                acknowledged:
                                    type: boolean
                                matched_count:
                                    type: string
                                modified_count:
                                    type: integer
                                upserted_id:
                                    type: integer
            '500':
                description: Some error occured, check logs
        """
        obj = collection.replace_one({"_id": ObjectId(product_id)}, request.json )
        return obj

    def post(self):
        """
        Create a new object
        ---
        parameters:
            -   in: body
                description: Data which needs to be inserted
                schema:
                    type: object
                    properties:
                        name:
                            type: string
                        brand_name:
                            type: string
                        regular_price_value:
                            type: number
                            format: float
                        offer_price_value:
                            type: number
                            format: float
                        currency:
                            type: string
                        classification_l1:
                            type: string
                        classification_l2:
                            type: string
                        classification_l3:
                            type: string
                        classification_l4:
                            type: string
                        image_url:
                            type: string
        responses:
            '200':
                description: Object created sucessfully
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                ObjectId:
                                    type: string
            '500':
                description: Some error occured, check logs
        """
        id_ = collection.insert_one(request.json).inserted_id
        return {"ObjectId": str(id_)}

    def delete(self, product_id):
        """
        Delete an object
        ---
        parameters:
            -   in: path
                name: product_id
                description: Id of the object which will have it's values altered
                schema:
                    type: string
                required: true
        responses:
            '200':
                description: Object deleted successfully
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                message:
                                    type: string
            '500':
                description: Some error occured, chekc logs
        """
        count = collection.delete_one({"_id": ObjectId(product_id)}).deleted_count
        return {"message": "%s object deleted successfully" % str(count)}, 200
