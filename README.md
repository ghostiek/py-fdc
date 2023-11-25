# py-fdc
A python interface to interact with the USDA's FoodDataCentral API

## Requirements
- Python >=3.10 

## Dependencies
- [requests](https://pypi.org/project/requests/)
- [pyhumps](https://pypi.org/project/pyhumps/)

## Usage

```python
from fdc import FDC

# Initialize the client with your API key
client = FDC(api_key)

# Get Food using FDCId
food = client.get_food(fdc_id)

# Get multiple Foods using a list of FDCIds
foods = client.get_foods([fdc_id1, fdc_id2, fdc_id3])

# Get a paged list of foods
food_list = client.get_foods_list()

# Search foods using keywords, in this case, get 200 cheese items
cheeses = client.get_foods_search("cheese")

# The USDA's FoodDataCentral API can be quite inconsistent at times, I've tried mapping it the best I could but if it
# results in an error, you can always just get the json string using the raw parameter
# Here is the equivalent to the above, except the output is a str
food_raw = client.get_food_raw(fdc_id)
foods_raw = client.get_foods_raw([fdc_id1, fdc_id2, fdc_id3])
food_list_raw = client.get_foods_list_raw()
cheeses_raw = client.get_foods_search_raw("cheese")
```

## API Documentation
More information about the API is available [here](https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1)


