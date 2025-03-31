from typing import Any, Type, TypeVar

from polyfactory.factories.pydantic_factory import ModelFactory as PydanticModelFactory
from pydantic import BaseModel

from fluree_py.client import FlureeClient
from fluree_py.query.select.pydantic import from_pydantic

T = TypeVar("T", bound=BaseModel)


def create_and_retrieve_random_model(
    model_class: Type[T],
    fluree_client: FlureeClient,
    ledger_name: str,
    extra_context: dict[str, Any] = {},
) -> tuple[T, T]:
    """
    Create a Pydantic model, insert it into Fluree, and retrieve it.

    Args:
        model_class: The Pydantic model class to test
        fluree_client: The Fluree client to use
        ledger_name: The name of the ledger to use
        cleanup_nested_ids: Whether to remove id fields from nested models before comparison

    Returns:
        A tuple containing (original_model, retrieved_model)
    """
    # Build a test model
    model = PydanticModelFactory.create_factory(
        model=model_class, __allow_none_optionals__=False
    ).build()

    return (
        model,
        create_and_retrieve_model(model, fluree_client, ledger_name, extra_context),
    )


def create_and_retrieve_model(
    model_instance: T,
    fluree_client: FlureeClient,
    ledger_name: str,
    extra_context: dict[str, Any] = {},
) -> T:
    """
    Create a Pydantic model, insert it into Fluree, and retrieve it.

    Args:
        model_class: The Pydantic model class to test
        fluree_client: The Fluree client to use
        ledger_name: The name of the ledger to use
        cleanup_nested_ids: Whether to remove id fields from nested models before comparison

    Returns:
        A tuple containing (original_model, retrieved_model)
    """
    # Create final context
    context = {"id": "@id"}
    context.update(extra_context)

    # Create a new ledger and insert the model
    fluree_client.with_ledger(ledger=ledger_name).create().with_context(
        context
    ).with_insert([model_instance.model_dump()]).commit()

    # Get the model back from the ledger
    model_id = model_instance.id  # type: ignore
    resp = (
        fluree_client.with_ledger(ledger=ledger_name)
        .query()
        .with_context(context)
        .with_where([{"@id": "?s"}, ["filter", f'(= ?s "{model_id}")']])
        .with_select(fields={"?s": from_pydantic(type(model_instance))})
        .commit()
    )

    # Parse the response into a model
    result_model = model_instance.model_validate_json(resp.text)

    return result_model
