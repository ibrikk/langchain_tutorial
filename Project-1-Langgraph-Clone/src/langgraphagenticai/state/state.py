from typing_extensions import Annotated, TypedDict, list
from langgraph.graph.message import add_messages

class State(TypedDict):
    message: Annotated[list, add_messages]