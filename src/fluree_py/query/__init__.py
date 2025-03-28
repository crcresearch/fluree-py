from typing import Any
from pydantic import BaseModel


# TODO: Implement query builder
# An example of a query is:
# {
#   "select": ["?company", "?name"],
#   "where": {
#     "@id": "?s",
#     "ex:name": "?name",
#     "ex:company": "?company"
#   },
#   "groupBy": "?company"
# }

# Select defines the fields to be returned
# Where defines the conditions for the query
# GroupBy defines the field to group the results by

# Queries should validate the variables used in the query
