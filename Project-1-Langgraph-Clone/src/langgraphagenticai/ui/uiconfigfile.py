from configparser import ConfigParser

class Config:
    def __init__(self, config_file="/Users/ibrahimkhalilov/Documents/langchain_tutorial/Project-1-Langgraph-Clone/src/langgraphagenticai/ui/uiconfigfile.ini"):
        self.config=ConfigParser()
        self.config.read(config_file)
    
    def get_llm_options(self):
        # print(self.config["DEFAULT"].get("LLM_OPTIONS"))
        return self.config["DEFAULT"].get("LLM_OPTIONS")
    
    def get_usecase_options(self):
        # print(self.config["DEFAULT"].get("USECASE_OPTIONS").split(", "))
        return self.config["DEFAULT"].get("USECASE_OPTIONS").split(", ")
    
    def get_groq_model_options(self):
        # print(self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(", "))
        return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(", ")
    
    def get_page_title(self):
        # print(self.config["DEFAULT"].get("PAGE_TITLE"))
        return self.config["DEFAULT"].get("PAGE_TITLE")
