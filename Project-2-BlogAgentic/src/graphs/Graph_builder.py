from langgraph.graph import StateGraph, START, END
from src.llms.Groqllm import GroqLLM
from src.states.Blogstate import BlogState
from src.nodes.BlogNode import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)
        
    def build_topic_graph(self):
        
        self.blog_node_object = BlogNode(llm=self.llm)
        
        self.graph.add_node("title_creation", self.blog_node_object.title_creation)
        self.graph.add_node("content_generator", self.blog_node_object.content_generator)
        
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generator")
        self.graph.add_edge("content_generator", END)
        
        return self.graph
    
    def build_language_graph(self):
        self.blog_node_object = BlogNode(llm=self.llm)
        self.graph.add_node("title_creation", self.blog_node_object.title_creation)
        self.graph.add_node("content_generator", self.blog_node_object.content_generator)
        self.graph.add_node("route_title", self.blog_node_object.route)
        self.graph.add_node("aze_translation_title", lambda state: self.blog_node_object.translation_of_title(
            {**state, "current_language": "azerbaijani"}
            ))
        self.graph.add_node("french_translation_title", lambda state: self.blog_node_object.translation_of_title(
            {**state, "current_language": "french"}
        ))
        
        self.graph.add_node("aze_translation", lambda state: self.blog_node_object.translation(
            {**state, "current_language": "azerbaijani"}
        ))
        self.graph.add_node("french_translation", lambda state: self.blog_node_object.translation(
            {**state, "current_language": "french"}
            ))
        self.graph.add_node("route", self.blog_node_object.route)
        
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generator")
        self.graph.add_edge("content_generator", "route_title")
        self.graph.add_conditional_edges("route_title",
                                         self.blog_node_object.route_decision,
                                         {
                                             "azerbaijani": "aze_translation_title",
                                             "french": "french_translation_title",
                                         }
                                         )
        self.graph.add_edge("aze_translation_title", "route")
        self.graph.add_edge("french_translation_title", "route")
        self.graph.add_conditional_edges("route",
                                         self.blog_node_object.route_decision,
                                         {
                                             "azerbaijani": "aze_translation",
                                             "french": "french_translation",
                                         }
                                         )
        
        self.graph.add_edge("aze_translation", END)
        self.graph.add_edge("french_translation", END)
        
        return self.graph
    
    def setup_graph(self, usecase):
        if usecase == "topic":
            self.build_topic_graph()
        elif usecase == "language":
            print("Language block")
            self.build_language_graph()
        
        return self.graph.compile()
    
llm = GroqLLM().get_llm()
graph_builder = GraphBuilder(llm)
graph = graph_builder.build_language_graph().compile()
    