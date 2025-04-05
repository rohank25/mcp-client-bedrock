from .client import ChatClient


def main():
    chat = ChatClient(
        aws_profile = "dio",
        aws_region = "us-east-1",
        model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    )

    chat.start()

if __name__ == "__main__":
    main()