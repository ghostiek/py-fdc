# py-fdc
A python interface to interact with the USDA's FoodDataCentral API

## Features
- An object oritented interface for FoodDataCentral's 

## Requirements
- Python >=3.10

## Dependencies
- [requests](https://pypi.org/project/requests/)
- [pyhumps](https://pypi.org/project/pyhumps/)

### Development Dependencies
- [PDM](https://pdm-project.org/latest/)
- [pytest](https://pypi.org/project/pytest/)
- [sphinx](https://pypi.org/project/Sphinx/)

## Installation

The simplest way to install it is to pip install it.

```bash
pip install py-usda-fdc
```

To install the development version you can pip the git version.
```bash
pip install git+https://github.com/ghostiek/py-fdc.git
```

## Getting Started

### Get an API Key

An API Key is necessary to make calls to USDA's API. You can get one by filling in this 
[form](https://fdc.nal.usda.gov/api-key-signup.html).

```python
# Import the FDC module
from fdc.fdc import FDC

# Initialize the client with your API key
client = FDC(api_key)
```

### Getting the Serialized output from the API

```python
# Get Food using FDCId
food = client.get_food(fdc_id) # Returns a Food object

# Get multiple Foods using a list of FDCIds
foods = client.get_foods([fdc_id1, fdc_id2, fdc_id3]) # Returns a list of Food objects

# Get a paged list of foods
food_list = client.get_foods_list() # Returns a list of AbridgedFood

# Search foods using keywords, in this case, get 200 cheese items
cheeses = client.get_foods_search("cheese") # Returns a SearchResult object
```

### Getting the Raw JSON as a string

Unfortunately, the USDA's FoodDataCentral API can be quite inconsistent at times, I've tried mapping it the best I could but if it
results in an error, you can always just get the json string using the raw parameter
Here is the equivalent of the functions referenced previously, except the output is a string.

```python
# All of them are strings
food_raw = client.get_food_raw(fdc_id)
foods_raw = client.get_foods_raw([fdc_id1, fdc_id2, fdc_id3])
food_list_raw = client.get_foods_list_raw()
cheeses_raw = client.get_foods_search_raw("cheese")
```

## API Documentation
More information about the API is available [here](https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1)


