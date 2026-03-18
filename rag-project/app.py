import gradio as gr
from workflow import rag_engine

tech_css = """
/* יישור לימין ופונט נקי */
.gradio-container { direction: rtl; font-family: 'Inter', sans-serif !important; }
#header-text { text-align: center; padding: 20px; }

/* תיקון צבעי הטקסט בתוך הבועות (Gradio עוטף הכל בפסקאות) */
.message.user { background-color: #2563eb !important; border: none !important; } 
.message.user p { color: #ffffff !important; font-size: 15px !important; } /* טקסט לבן בוהק למשתמש */

.message.bot { background-color: #334155 !important; border: none !important; } 
.message.bot p { color: #ffffff !important; font-size: 15px !important; } /* טקסט לבן בוהק לבוט */

/* עיצוב תיבת הטקסט התחתונה */
#query-input textarea { font-size: 15px !important; border-radius: 8px !important; }
"""

async def chat_response(message, history):
    try:
        response = await rag_engine.run(query=message)
        return str(response)
    except Exception as e:
        return f"שגיאה בתהליך העיבוד: {str(e)}"

with gr.Blocks(css=tech_css, theme=gr.themes.Soft()) as demo:
    with gr.Row(elem_id="header-text"):
        gr.Markdown("""
        # 💠 PROJECT KNOWLEDGE GRAPH
        **Advanced RAG Interface | Cohere Command-R-Plus**
        """)
    
    with gr.Column():
        chatbot = gr.Chatbot(show_label=False, height=550)
        chat_interface = gr.ChatInterface(
            fn=chat_response,
            chatbot=chatbot,
            textbox=gr.Textbox(
                placeholder="הזן שאילתה טכנית לניתוח הנתונים...", 
                elem_id="query-input",
                container=False, 
                scale=7
            ),
            submit_btn="הרץ שאילתה",
            stop_btn="עצור"
        )

if __name__ == "__main__":
    print("🚀 מתחיל את השרת המקומי...")
    demo.launch()