import gradio as gr
from agent import CodingAgent

agent = CodingAgent()

def chat_interface(user_message, context_file=None):
    return agent.handle_instruction(user_message, context_file)

demo = gr.Interface(
    fn=chat_interface,
    inputs=[
        gr.Textbox(lines=4, label="Your Message"),
        gr.Textbox(label="Optional Context File Path")
    ],
    outputs="text",
    title="💬 AI Coding Assistant",
    description="Ask the AI to generate or modify code. Optionally give a filename to use its content."
)

demo.launch()
