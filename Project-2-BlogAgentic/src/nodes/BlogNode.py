from src.states.Blogstate import BlogState, Blog
from langchain_core.messages import HumanMessage

class BlogNode:
    def __init__(self, llm):
        self.llm = llm
    
    def title_creation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            prompt = """
            You are an expert blog content writer. Use Markdown formatting. 
            Generate a blog title for the {topic}. This title should be creative and SEO friendly
            """
            
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": response.content}}
    
    def content_generator(self, state: BlogState):
        if "topic" in state and state["topic"] and state["blog"]["title"]:
            system_prompt = """
            You are expert blog writer. Use Markdown formatting. 
            Generate a detailed blog content with detailed breakdown for the {topic}
            """
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state["blog"]["title"], 
                             "content": response.content}}
            
        
            
    def translation(self, state: BlogState):
        if "current_language" in state and state["current_language"]:
            prompt = """
            Translate the following content into {language}. 
            - Maintain the original tone, style, and formatting.
            - Adapt cultural references and idioms to be appropriate for {language}
            
            ORIGINAL CONTENT:
            {blog_content}
            """
            
            messages = [
                HumanMessage(prompt.format(language=state["current_language"], 
                                           blog_content=state["blog"]["content"]))
                
            ]
            # translation_content = self.llm.with_structured_output(Blog).invoke(messages)
            response = self.llm.invoke(messages)
            return {"blog": {
                        "title":  state["blog"]["title"], 
                        "content": response.content
                            }, 
                    "current_language": state.get("current_language")}
    
    def translation_of_title(self, state: BlogState):
        if "current_language" in state and state["current_language"]:
            prompt = """
            Translate the following content into {language}. 
            - Maintain the original tone, style, and formatting.
            - Adapt cultural references and idioms to be appropriate for {language}
            
            ORIGINAL CONTENT:
            {title}
            """
            
            messages = [
                HumanMessage(prompt.format(language=state["current_language"], 
                                           title=state["blog"]["title"]))
                
            ]
            # translation_content = self.llm.with_structured_output(Blog).invoke(messages)
            response = self.llm.invoke(messages)
            return {"blog": {
                        "title":   response.content,
                        "content": state["blog"]["content"]
                            }, 
                    "current_language": state.get("current_language")}
    
            
    def route(self, state: BlogState):
        return {"current_language": state.get("current_language")} 
    
    def route_decision(self, state: BlogState):
        if state["current_language"] == "azerbaijani":
            return "azerbaijani"
        elif state["current_language"] == "french":
            return "french"
        else:
            return state["current_language"]
            