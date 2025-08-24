from typing_extensions import Annotated, TypedDict, List
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[List, add_messages]