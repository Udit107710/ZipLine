# ZipLine
This app contains APIs which will allow you to perform CRUD operations on your MongoDB Clusters
<hr>
<br>

## Supported Features
- [x] CREATE a single product
- [x] CREATE multiple products
- [x] RETRIEVE a single product
- [x] RETRIEVE multiple products
- [x] UPDATE a single product
- [x] UPDATE multiple products
- [x] DELETE a single product
- [x] DELETE multiple products
- [x] Detailed documentation
- [x] Support for pagination
- [x] Versioning flexibility
- [ ] Multiple operations in a single query
- [ ] Extensive logging
- [ ] Filter while fetching multiple objects
- [ ] Swagger UI
<br>
<b>*Object schema checking feature is not added to take advantage of NoSQL's schema indepenance*</b>
<hr>
<br>

## Installation
### Dependencies
1. [Docker Compose](https://docs.docker.com/compose/)
2. Internet connection to connect to Cluster

### Steps to run
```
git clone https://github.com/Udit107710/ZipLine.git
```
```
cd ZipLine
```
```
docker-compose up
```
<hr>
<br>

## Endpoints
<br>

**PATCH will replace particular fields whereas PUT will replace whole object**

|URL|Method|Parameters|Response|
|---|---|---|---|
|/| GET | | HTML page to display documentation|
|api/v1/product/<product_id>| GET |<ol><li> product_id (in URL)</li></ol>| [Product (with ID)](#product-with-id)|
|api/v1/product/ | POST |<ol><li> [Product](#product) (in body)</li></ol>| [Message](#create-message)|
|api/v1/product/<product_id>| PATCH |<ol><li> product_id (in URL)</li><li>[Product](#product) (in body)</li></ol>| [Update Message](#update-message)|
|api/v1/product/<product_id>| PUT |<ol><li> product_id (in URL)</li><li>[Product](#product) (in body)</li></ol>| [Update Message](#update-message)|
|api/v1/products | GET |<ol><li> skip<sup>1</sup> (in query)</li><li> limit<sup>2</sup> (in query)</li></ol>| [Products with details](##product-with-details)|
|api/v1/products | POST |<ol><li> Array of [Product](#product) (in body)</li></ol>| [Bulk Update Message](#bulk-write-message)|
|api/v1/products | PATCH |<ol><li> Array of [this](#edit-multiple-details) (in body)</li></ol>| [Bulk Update Message](#bulk-write-message)|
|api/v1/products | PUT |<ol><li> Array of [this](#edit-multiple-details) (in body)</li></ol>| [Bulk Update Message](#bulk-write-message)|

1: How many products to skip from start

2: How many products to fetch
<hr>
<br>

## Examples
### List with 5 elements skipped and 1 fetched
![001.png](zipline/images/001.png)
<br>
<br>

### List with 5 elements skipped and 2 fetched
![002.png](zipline/images/002.png)

Find postman collection [here](https://www.getpostman.com/collections/801dba9637c62c737893)

## Object Schemas

### Product
```
{
    'name':   <string>,
    'brand_name':   <string>,
    'regular_price_value':   <float>,
    'offer_price_value':   <float>,
    'currency':   <string>,
    'classification_l1':  <string>v,
    'classification_l2':   <string>,
    'classification_l3':   <string>,
    'classification_l4':   <string>,
    'image_url':   <string>,
}
```

### Product With Id
```
{
    '_id': <string>,
    'name':   <string>,
    'brand_name':   <string>,
    'regular_price_value':   <float>,
    'offer_price_value':   <float>,
    'currency':   <string>,
    'classification_l1':  <string>v,
    'classification_l2':   <string>,
    'classification_l3':   <string>,
    'classification_l4':   <string>,
    'image_url':   <string>,
}
```

### Create Message
```
{
    "ObjectId": <string>
}
```

### Update Message
```
{
    "acknowledged": <bool>,
    "matched_count": <int>,
    "modified_count": <int>,
    "upserted_id": <int>,
}
```

### Bulk Write Message
```
{
    "acknowledged": <bool>,
    "matched_count": <int>,
    "modified_count": <int>,
    "deleted_count": <int>,
    "inserted_count": <int>,
}
```

### Products with details
```
{
    "products": [
        ...
        {
            '_id': <string>,
            'name':   <string>,
            'brand_name':   <string>,
            'regular_price_value':   <float>,
            'offer_price_value':   <float>,
            'currency':   <string>,
            'classification_l1':  <string>v,
            'classification_l2':   <string>,
            'classification_l3':   <string>,
            'classification_l4':   <string>,
            'image_url':   <string>,
        },
        ...
    ]
    "skip": <int>,
    "limit": <int>
}
```

### Edit Multiple Details
```
[
    ...
    {
		"_id": <string>,
		"data":
				{
                    ...
					<string>: <string>,
                    ...
				}
	}
    ...
]
```