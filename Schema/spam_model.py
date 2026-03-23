from pydantic import BaseModel,Field
from typing import Annotated

class spam_detection(BaseModel):
    input_text : Annotated[str,Field(...,description="Enter the Text of the Gmal/SMS,..etc",examples=["Limited time offer!!! Get 90% discount now!!!"])]