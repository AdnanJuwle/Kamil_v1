import sys
import signal
from typing import Optional

# Fix Windows encoding issues - must be before any imports that use print
if sys.platform == 'win32':
    import io
    try:
        # Check if we need to fix encoding (not already UTF-8)
        if hasattr(sys.stdout, 'buffer') and getattr(sys.stdout, 'encoding', '').lower() != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except (AttributeError, ValueError, TypeError):
        pass
    try:
        if hasattr(sys.stderr, 'buffer') and getattr(sys.stderr, 'encoding', '').lower() != 'utf-8':
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except (AttributeError, ValueError, TypeError):
        pass

from agent import CodingAgent

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\n\n👋 Goodbye!")
    sys.exit(0)

def main() -> None:
    """Main entry point for the AI Coding Assistant."""
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        agent = CodingAgent()
        print("📎 AI Coding Assistant (type 'exit' or 'quit' to quit)\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit"]:
                    print("👋 Goodbye!")
                    break

                # Ask user if they want to provide a file as context
                use_file = input("Do you want to provide a file for context? (y/n): ").lower().strip()
                context_file: Optional[str] = None
                
                if use_file == "y":
                    context_file = input("Enter file path: ").strip()
                    if not context_file:
                        context_file = None

                agent.handle_instruction(user_input, context_file=context_file)
                print()  # Add spacing between interactions
                
            except EOFError:
                # Handle Ctrl+D
                print("\n👋 Goodbye!")
                break
            except KeyboardInterrupt:
                # Handle Ctrl+C
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("Continuing...\n")
                
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
