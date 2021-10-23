from __future__ import annotations

class GraphFilter:
    """Implements the IGraphFilter protocol."""
    
    def __init__(self, filter:str, value:str):
        self.filter = filter
        self.value = value
        self.subfilters:list[GraphFilter] = []

    def add_subfilter(self, filter:GraphFilter):
        self.subfilters.append(filter)
    
    def compose(self) -> str:
        result = f"${self.filter}={self.value}"
        if len(self.subfilters) < 1:
            return result
        result += "("
        for filter in self.subfilters:
            result += filter.compose()
        result += ")"
        return result