import os
from typing import Dict
from modal import web_endpoint, App, Secret, Image
from magentic import OpenaiChatModel, chatprompt, UserMessage

app = App("bookkeeper-api")
magentic_image = Image.debian_slim().pip_install("magentic>=0.24.0", "fastapi>=0.111.0")


@app.function(image=magentic_image, secrets=[Secret.from_name("openai")])
@web_endpoint(method="POST")
def message(item: Dict) -> str:
    @chatprompt(
        UserMessage(item["msg"] or "Say hi if you can hear me!"),
        model=OpenaiChatModel("gpt-4o", api_key=os.environ["OPENAI_API_KEY"]),
    )
    def message() -> str: ...

    return message()
