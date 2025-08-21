from typing_extensions import Annotated, TypedDict, list
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]