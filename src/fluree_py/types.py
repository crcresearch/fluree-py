"""Common type definitions for the fluree-py package.

This module provides type aliases for JSON-serializable data structures used throughout
the fluree-py package. These types are used to ensure type safety when working with
Fluree's JSON-based API.

Types:
    JsonObject: A dictionary with string keys and any JSON-serializable values.
               Used for representing JSON objects in Fluree queries and responses.
               
    JsonArray: A list of any JSON-serializable values.
               Used for representing JSON arrays in Fluree queries and responses.

Examples:
    >>> # JsonObject example
    >>> query: JsonObject = {
    ...     "select": ["*"],
    ...     "where": {"@id": "?s"}
    ... }
    
    >>> # JsonArray example
    >>> results: JsonArray = [
    ...     {"@id": "person/1", "name": "John"},
    ...     {"@id": "person/2", "name": "Jane"}
    ... ]
"""

from typing import Any, TypeAlias

# Type alias for JSON-serializable data that can be either a single dict or a list of dicts
JsonObject: TypeAlias = dict[str, Any]
JsonArray: TypeAlias = list[Any]