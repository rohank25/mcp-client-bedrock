from pydantic import BaseModel, PrivateAttr
from typing import List, Optional, Dict
import boto3
from mcp_client_bedrock.tools import BedrockToolManager

class Conversation(BaseModel):
    _client: boto3.client = PrivateAttr()
    _model: Optional[str] = PrivateAttr(default="us.anthropic.claude-3-5-sonnet-20241022-v2:0")
    _message_history: Optional[List] = PrivateAttr(default_factory=list)
    _tools: BedrockToolManager = PrivateAttr(default_factory=BedrockToolManager)
    _system_prompt: Optional[str] = PrivateAttr(
        default=[{
            "text": """
            You are a Senior Site Relibility Engineer at a fast-growing, cloud-native digital bank.
            You are intimately familiar with distributed, event-driven microservice architectures.
            """
        }])
    _model_temperature: float = PrivateAttr(default=0.5)
    _model_top_k: int = PrivateAttr(default=200)

    def __init__(self, client: boto3.client, **data):
        super().__init__(**data)
        self._client = client  # Initialize the private client attribute

    @property
    def message_history(self) -> List[str]:
        return self._message_history
    
    @property
    def tools(self) -> List[str]:
        return self._tools
    
    @property
    def system_prompt(self) -> str:
        return self._system_prompt
    
    @message_history.setter
    def update_message_history(self, value: Dict) -> None:
        self._message_history.append(value)

    @tools.setter
    def tools(self, value: List[str]) -> None:
        self._tools = value

    def invoke(self, message: str) -> str:
        self.update_message_history = {
            "role": "user",
            "content": [{
                'text': message
            }]
        }
        response = self._client.converse(
            modelId = self._model,
            messages = self._message_history,
            system = self._system_prompt,
            inferenceConfig = {
                "temperature": self._model_temperature
            },
            additionalModelRequestFields={
                "top_k": self._model_top_k
            },
            toolConfig = self.tools()
        )
        self.update_message_history = response["output"]["message"]
        print(f"------- SYSTEM RESPONSE TYPE: {response["stopReason"]}")


        return response["output"]["message"]["content"][0]["text"]