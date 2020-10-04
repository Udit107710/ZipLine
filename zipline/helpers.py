from flask_restful import fields

def modify_product(product):
    product['_id'] = str(product['_id'])
    return product

def modify_products(products):
    for p in products:
        p['_id'] = str(pp['_id'])
    
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
    "upserted_id": fields.Integer,
    "deleted_count": fields.Integer,
}