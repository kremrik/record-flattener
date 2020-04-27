from typing import Any, List, Union


__all__ = [
    "flatten"
]


def flatten(
    record: dict, 
    parent_key: str = "", 
    output: dict = None, 
    sep: str = ".",
    parse_lists: bool = False,
    list_key_id: str = None,
    full_list_flatten: bool = False
    ) -> dict:
    """
    :param record:              a Python dict object
    :param parent_key:          the key name of the parent level
    :param output:              the flattened dict object
    :param sep:                 the desired separator for concatenated parent/child keys
    :param parse_lists:         flag for whether to flatten lists of dicts (one level only)
    :param list_key_id:         the key name of the unique value for converting to a flattened dict key (only valid if `parse_lists` is True)
    :param full_list_flatten:   flag for whether to fully flatten lists of dicts (only valid if `list_key_id` is set)
    """
    if parse_lists:
        assert list_key_id, "if 'parse_lists' is True, 'list_key_id' must not be None"
    if list_key_id:
        assert parse_lists, "'parse_lists' must not be False if 'list_key_id' is set"
    if full_list_flatten:
        assert list_key_id, "if 'full_list_flatten' is True, 'list_key_id' must be set"
        assert parse_lists, "if 'full_list_flatten' is True, 'parse_lists' must be set to True"

    if not record:
        return record

    if not output:
        output = {}

    for key, value in record.items():
        this_key = parent_key + key
        next_key = this_key + sep

        if _is_dict(value):
            output = flatten(record=value, parent_key=next_key, output=output)

        elif _is_list(value) and parse_lists:
            flat_list = _flatten_list(records=value, list_key_id=list_key_id)

            # second check to make sure we don't try to flatten an empty list
            if full_list_flatten and flat_list:
                return flatten(record=flat_list, parent_key=next_key, output=output)

            output[this_key] = flat_list

        else:
            output[this_key] = value

    return output


def _flatten_list(records: list, list_key_id: str) -> Union[dict, list]:
    if not records:
        return records

    # TODO: assumes homogeneous types within list
    if _is_primitive(records[0]):
        return records

    output = {}

    for record in records:
        this_key = record[list_key_id]
        output[this_key] = _lift_key(record, list_key_id)

    return output


def _lift_key(record: dict, list_key_id: str) -> dict:
    return {
        k: v
        for k, v in record.items()
        if k != list_key_id
        }


def _is_obj(obj: Any, check_type: type) -> bool:
    return isinstance(obj, check_type)


def _is_dict(obj: Any) -> bool:
    return _is_obj(obj, dict)


def _is_list(obj: Any) -> bool:
    return _is_obj(obj, list)


def _is_primitive(obj: Any) -> bool:
    return not _is_dict(obj) and not _is_list(obj)
