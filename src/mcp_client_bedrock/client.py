from pydantic import BaseModel, Field, PrivateAttr
import os
import boto3
import traceback
from mcp_client_bedrock.conversation import Conversation


class ChatClient(BaseModel):
    aws_profile: str = Field(default_factory=lambda: os.getenv, env="AWS_PROFILE")
    aws_region: str = Field(default_factory=lambda: os.getenv, env="AWS_REGION")
    model_name: str = Field(default_factory=lambda: os.getenv, env="MODEL_ID")
    _client: boto3.client = PrivateAttr(default=None)
    _conversation: Conversation = PrivateAttr(default=None)
    
    def __init__(self, **data):
        super().__init__(**data)
        session = boto3.Session(profile_name=self.aws_profile, region_name=self.aws_region)
        self._client = session.client("bedrock-runtime")
        self._conversation = Conversation(
            client=self._client,
            model=self.model_name
        )

    def send_message(self, message: str) -> str:
        if not self._client:
            raise ValueError("Agent is not initialized. Ensure the Bedrock client and model are properly set up.")
        try:
            response = self._conversation.invoke(message)
            return response
        except Exception as e:
            print(f"------- SYSTEM ERROR: {e}")
            traceback.print_exc()
            raise

    def start(self) -> None:
        # Simulate sending a message to the chat model and receiving a response
        print("Starting Chat session...")
        while True: 
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Ending chat session... Goodbye!")
                break
            try:
                response = self.send_message(user_input)
            except Exception as e:  
                print(f"------- SYSTEM ERROR: {e}")
                traceback.print_exc() 
                continue
            print(f"Bot: {response}")