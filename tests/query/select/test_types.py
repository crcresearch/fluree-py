from typing import Any

from hypothesis import assume, example, given
from hypothesis import strategies as st

from fluree_py.types.query.select import (
    is_logic_variable,
    is_node_object_template,
    is_select_array,
    is_select_array_element,
    is_select_object,
)

# Test LogicVariable
logic_variable_strategy = st.from_regex(r"\?[a-zA-Z0-9_-]+", fullmatch=True)


@given(logic_variable_strategy)
@example("?firstname")
@example("?first-name")
@example("?first_name")
@example("?address-1")
def test_logic_variable(val: str) -> None:
    assume(all(c.isprintable() for c in val))
    assert is_logic_variable(val)


# Test NodeObjectTemplate
select_expression_strategy = st.one_of(
    st.just("*"),
    st.text(),
    st.dictionaries(keys=st.text(), values=st.lists(st.one_of(st.just("*"), st.text()), min_size=1)),
)

select_expression_list_strategy = st.lists(select_expression_strategy, min_size=1)
node_object_template_strategy = st.dictionaries(keys=st.text(min_size=1), values=select_expression_list_strategy)


@given(node_object_template_strategy)
@example({"schema:address": ["*"]})  # Get all address predicates
@example({"bestFriend": ["*"]})  # Get all best friend predicates
@example({"bestFriend": [{"address": ["*"]}]})  # Get address of best friend
def test_node_object_template_valid(template: dict[str, Any]) -> None:
    assert is_node_object_template(template)


# Test SelectObject
select_object_strategy = st.dictionaries(keys=logic_variable_strategy, values=select_expression_list_strategy)


@given(select_object_strategy)
@example({"?s": ["name", {"bestFriend": ["*"]}]})  # Get name and all predicates of best friend
def test_select_object_valid(obj: dict[str, Any]) -> None:
    assert is_select_object(obj)


# Test SelectArrayElement
select_array_element_strategy = st.one_of(logic_variable_strategy, select_object_strategy)


@given(select_array_element_strategy)
@example("?s")
@example({"?s": ["*"]})
@example({"?friend": ["*"]})
def test_select_array_element_valid(element: str | dict[str, Any]) -> None:
    assert is_select_array_element(element)


# Test SelectArray
select_array_strategy = st.lists(select_array_element_strategy, min_size=1)


@given(select_array_strategy)
@example(["?s", "?name", "?friend"])  # Get multiple variables
@example([{"?s": ["*"]}, {"?friend": ["*"]}])  # Get multiple objects
def test_select_array_valid(arr: list[str | dict[str, Any]]) -> None:
    assert is_select_array(arr)
