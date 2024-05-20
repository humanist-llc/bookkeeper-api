from enum import Enum
from modal import web_endpoint, App, Secret, Image

from typing import Optional, Union, Dict

from pydantic import BaseModel, Field
from magentic import chatprompt, OpenaiChatModel, SystemMessage
from magentic.vision import UserImageMessage

from fastapi import Form

app = App("bookkeeper-api")
magentic_image = Image.debian_slim(python_version="3.12").pip_install(
    "magentic>=0.24.0", "fastapi>=0.111.0", "requests"
)


class Category(Enum):
    GROCERIES = "Groceries"
    DINING_OUT = "Dining Out"
    UTILITIES = "Utilities"
    TRANSPORTATION = "Transportation"
    HOUSING = "Housing"
    HEALTHCARE = "Healthcare"
    PERSONAL_CARE = "Personal Care"
    ENTERTAINMENT = "Entertainment"
    CLOTHING_ACCESSORIES = "Clothing & Accessories"
    ELECTRONICS = "Electronics"
    EDUCATION = "Education"
    GIFTS_DONATIONS = "Gifts & Donations"
    TRAVEL = "Travel"
    SAVINGS_INVESTMENTS = "Savings & Investments"
    MISCELLANEOUS = "Miscellaneous"

    @classmethod
    def _missing_(cls):
        return cls.MISCELLANEOUS


class ReceiptDetails(BaseModel):
    vendor: str = Field(
        description="The name of the vendor.",
        examples=["Walmart"],
        default="Not detected",
    )
    transaction_date: str = Field(
        description="The date the transaction was conducted.",
        examples=["2022-01-01"],
        default="Not detected",
    )
    goods: Union[Dict[str, float], str] = Field(
        description="Identify the products purchased in the transaction, include the amount as well as their costs. Be concise.",
        examples=[{"1x Dorito": 1.99}],
        default={},
    )
    total: float = Field(
        description="The total amount paid in the transaction. Output 0.00 when not detected.",
        examples=[1.99],
        default=[0.00],
    )
    category: Category = Field(
        description="Classify this transactions nature.",
        examples=[Category.GROCERIES],
        default=Category.MISCELLANEOUS,
    )


class Response(BaseModel):
    receipt: Optional[ReceiptDetails]
    error: Optional[str]


@app.function(image=magentic_image, secrets=[Secret.from_name("openai")])
@web_endpoint(method="POST")
def extractReceipt(image: str = Form(...)) -> Response:
    if "image" not in image:
        return Response(receipt=None, error="No image provided.")

    # data = image["image"].encode()

    # @chatprompt(
    #     SystemMessage(
    #         "You are a receipt scanner, do not make up any information. Scan the receipt and provide the details."
    #     ),
    #     UserImageMessage(data),
    #     model=OpenaiChatModel("gpt-4o", temperature=1),
    # )
    # def describe_image() -> ReceiptDetails: ...

    # return Response(receipt=describe_image(), error=None)
    return Response(receipt=None, error="Test")
