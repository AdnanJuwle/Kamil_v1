from agent import CodingAgent
from dataset_utils import replace_known_datasets

def main():
    agent = CodingAgent()

    print("📎 AI Coding Assistant (type 'exit' to quit)\n")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # Ask user if they want to provide a file as context
        use_file = input("Do you want to provide a file for context? (y/n): ").lower()
        context_file = None
        if use_file == "y":
            context_file = input("Enter file path: ").strip()

        agent.handle_instruction(user_input, context_file=context_file)

if __name__ == "__main__":
    main()
