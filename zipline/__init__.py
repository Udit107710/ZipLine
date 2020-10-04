import os

from flask import Flask
from flask_restful import Api
from zipline.api import Home, ProductInstanceView, ProductListView


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DEBUG=test_config or False
    )
    api = Api(app)
    api.add_resource(Home, '/')
    api.add_resource(ProductListView, '/products', endpoint="products")
    api.add_resource(ProductInstanceView, '/product/<product_id>', methods=["GET", "PATCH", "PUT"], endpoint="productEdit")
    api.add_resource(ProductInstanceView, '/product/', methods=["POST"], endpoint="productCreate")

    return app