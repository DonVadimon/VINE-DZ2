from typing import Any, Dict, Iterable


def filterDict(d: Dict[Any, Any]):
    return dict(filter(lambda item: item[1] is not None, d.items()))


def dictEntries(d: Dict[Any, Any]):
    return list(d.items())


def dictKeys(d: Dict[Any, Any]):
    return list(d.keys())


def dictValues(d: Dict[Any, Any]):
    return list(d.values())


def listJoin(l: Iterable, delimeter: str):
    return delimeter.join(l)


def formatSQLValue(value: Any):
    if type(value) is str:
        return f"'{value}'"

    return f"{value}"
