from typing import Any
from textual.widgets import ListItem, Label

class ValueListItem(ListItem):
    value: Any

    def __init__(self, label: str, value: Any, **kwargs: Any) -> None:
        super().__init__(Label(label), **kwargs)
        self.value = value
