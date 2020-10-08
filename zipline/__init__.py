from flask import Flask
from flask_restful import Api
from flask import Flask, jsonify

from flask_swagger import swagger

from zipline.api import Home, ProductInstanceView, ProductListView


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DEBUG=test_config or False
    )

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "0.1"
        swag['info']['title'] = "ZipLine"
        return jsonify(swag)

    api = Api(app)
    # api.add_resource(Home, '/')
    api.add_resource(ProductListView, '/api/v1/products', endpoint="products")
    api.add_resource(ProductInstanceView, '/api/v1/product/<product_id>', methods=["GET", "PATCH", "PUT", "DELETE"], endpoint="productEdit")
    api.add_resource(ProductInstanceView, '/api/v1/product/', methods=["POST"], endpoint="productCreate")

    return app