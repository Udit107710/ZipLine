from flask_restful import fields
from pymongo.errors import BulkWriteError

def modify_product(product):
    """
    Convert ObjectId type to string
    """
    product['_id'] = str(product['_id'])
    return product

def modify_products(products):
    """
    Recursively convert ObjectId type to string
    """
    for p in products:
        modify_product(p)
    return products

resource_field_update = {
    "acknowledged": fields.Boolean,
    "matched_count": fields.Integer,
    "modified_count": fields.Integer,
    "upserted_id": fields.Integer,
}

resource_fields_product = {
    '_id':   fields.String,
    'name':   fields.String,
    'brand_name':   fields.String,
    'regular_price_value':   fields.Float,
    'offer_price_value':   fields.Float,
    'currency':   fields.String,
    'classification_l1':   fields.String,
    'classification_l2':   fields.String,
    'classification_l3':   fields.String,
    'classification_l4':   fields.String,
    'image_url':   fields.String,
}

resource_field_bulk_write = {
    "acknowledged": fields.Boolean,
    "matched_count": fields.Integer,
    "modified_count": fields.Integer,
    "deleted_count": fields.Integer,
    "inserted_count": fields.Integer,
}

def perform_bulk(collection, requests):
    """
    Common interface to perform bilk operations on a given collection.
    """
    try:
        obj = collection.bulk_write(requests, ordered=False)
    except BulkWriteError as bwe:
        print(bwe)
        return {"message": "Some error occured, check logs"}, 500
    return obj