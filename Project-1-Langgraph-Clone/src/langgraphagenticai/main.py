import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI

def load_langgraph_agenticai_app():
    # Load UI

    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI")
        return
    
    user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM could not be initialized.")
                return
            
            usecase = user_input.get("selected_usecase")
            if not usecase:
                st.error("Error: No use case selected")
                return
        except Exception as e:
            st.error(f"Error: Graph set up failed- {e}")
            return   

        
        
