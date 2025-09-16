#!/usr/bin/env python3

"""
Letter Prefix Pattern Generator with Tilde Prefix and Clipboard Support

This script takes input text and a list of user-defined prefixes, then uses regex
to add the prefixes (starting with '~') to each individual letter of the words, 
creating a repeating pattern. The output is formatted for easy copying.

Usage:
    python Colour-Pattern-Generator.py

Example:
    Input text: "Hello World!"
    Prefixes: ["W1", "W2"]
    Output: "~W1H~W2e~W1l~W2l~W1o~W2 ~W1W~W2o~W1r~W2l~W1d~W2!"

Requirements:
    pip install pyperclip (optional, for clipboard support)
"""

import re
import sys

# Try to import pyperclip for clipboard functionality
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
    print("✓ Clipboard support available")
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("⚠ Clipboard support not available (install with: pip install pyperclip)")

def ensure_tilde_prefix(prefixes):
    """
    Ensure all prefixes start with '~'. Add it if missing.
    
    Args:
        prefixes (list): List of prefix strings
    
    Returns:
        list: List of prefixes guaranteed to start with '~'
    """
    tilde_prefixes = []
    for prefix in prefixes:
        if not prefix.startswith('~'):
            tilde_prefixes.append('~' + prefix)
        else:
            tilde_prefixes.append(prefix)
    return tilde_prefixes

def add_prefixes_to_letters(text, prefixes):
    """
    Add alternating tilde prefixes to each letter in the text using regex.
    
    Args:
        text (str): Input text to process
        prefixes (list): List of prefix strings (will be ensured to start with ~)
    
    Returns:
        str: Text with tilde prefixes added to each letter
    """
    if not text or not prefixes:
        return text
    
    # Ensure all prefixes start with '~'
    tilde_prefixes = ensure_tilde_prefix(prefixes)
    
    # Count total letters in the text to determine how many prefixes we need
    total_letters = len(re.findall(r'\w', text))
    
    # Create enough repetitions of prefixes to cover all letters
    repetitions_needed = (total_letters // len(tilde_prefixes)) + 1
    extended_prefixes = tilde_prefixes * repetitions_needed
    
    # Create iterator from the extended prefix list
    prefix_iter = iter(extended_prefixes)
    
    # Pattern matches any word character (letters and digits)
    pattern = r'\w'
    
    # Replacement function that prepends the next tilde prefix to each matched letter
    def replacer(match):
        try:
            return next(prefix_iter) + match.group(0)
        except StopIteration:
            # Fallback if somehow we run out of prefixes
            return match.group(0)
    
    # Replace each letter with prefixed letter, preserve everything else
    return re.sub(pattern, replacer, text)

def copy_to_clipboard(text):
    """
    Copy text to clipboard if pyperclip is available.
    
    Args:
        text (str): Text to copy to clipboard
    
    Returns:
        bool: True if successfully copied, False otherwise
    """
    if not CLIPBOARD_AVAILABLE:
        return False
    
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return False

def display_copyable_output(original_text, result, prefixes):
    """
    Display the result in an easily copyable format.
    
    Args:
        original_text (str): Original input text
        result (str): Processed text with tilde prefixes
        prefixes (list): List of prefixes used
    """
    print("\n" + "=" * 60)
    print("COPYABLE OUTPUT")
    print("=" * 60)
    
    # Display original for reference
    print(f"Original: {original_text}")
    print(f"Colours: {prefixes}")
    print()
    
    # Display result in a copyable text box
    print("📋 RESULT (ready to copy):")
    print("┌" + "─" * 58 + "┐")
    
    # Split long results into multiple lines if needed
    max_width = 56
    if len(result) <= max_width:
        print(f"│ {result:<{max_width}} │")
    else:
        # Split into chunks that fit the box
        words = result.split(' ')
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_width:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    print(f"│ {current_line:<{max_width}} │")
                current_line = word
        
        if current_line:
            print(f"│ {current_line:<{max_width}} │")
    
    print("└" + "─" * 58 + "┘")
    
    # Try to copy to clipboard
    if copy_to_clipboard(result):
        print("✅ Automatically copied to clipboard!")
    else:
        print("📝 Select and copy the text above manually")
    
    # Provide raw text section for manual copying
    print(f"\n🔤 Raw text for manual copy:")
    print("-" * 40)
    print(result)
    print("-" * 40)
    
    # Statistics
    letter_count = len(re.findall(r'\w', original_text))
    print(f"\n📊 Statistics:")
    print(f"   • Original letters: {letter_count}")
    print(f"   • Result length: {len(result)} characters")
    print(f"   • Colour codes used: {len(set(ensure_tilde_prefix(prefixes)))}")

def get_user_input():
    """Get input text and prefixes from user."""
    print("🌊 Colour Code Pattern Generator")
    print("=" * 40)
    print("All codes will automatically start with '~'")
    
    # Get input text
    input_text = input("\n📝 Enter your text: ").strip()
    if not input_text:
        print("❌ Error: Please enter some text.")
        return None, None
    
    # Get prefixes
    print("\n🏷️  Enter prefixes separated by commas.")
    print("Examples: '~W1,~W2' or 'R5,O5,Y5,G5,B5,M5,V5'")
    print("(Note: '~' will be automatically added if missing)")
    prefix_input = input("Colour Codes: ").strip()
    
    if not prefix_input:
        print("❌ Error: Please enter at least one colour code.")
        return None, None
    
    # Parse prefixes, removing empty strings
    prefixes = [p.strip() for p in prefix_input.split(',') if p.strip()]
    
    if not prefixes:
        print("❌ Error: No valid colour codes found.")
        return None, None
    
    return input_text, prefixes

def demonstrate_examples():
    """Show some example transformations with tilde prefixes."""
    examples = [
        ("Hello World!", ["A", "B"]),
        ("Python123", ["1", "2"]),
        ("Test", ["red", "blue", "green"]),
        ("Regex!", ["X", "Y", "Z"]),
    ]
    
    print("\n" + "=" * 60)
    print("EXAMPLES WITH TILDE PREFIXES - Each letter gets a prefix starting with '~'")
    print("=" * 60)
    
    for text, prefixes in examples:
        result = add_prefixes_to_letters(text, prefixes)
        tilde_prefixes = ensure_tilde_prefix(prefixes)
        print(f"Text: '{text}'")
        print(f"Input prefixes: {prefixes}")
        print(f"Tilde prefixes: {tilde_prefixes}")
        print(f"Result: '{result}'")
        print("-" * 50)

def main():
    """Main function to run the tilde prefix generator."""
    print("Welcome to the Tilde Prefix Pattern Generator! 🌊")
    
    while True:
        print("\n📋 Options:")
        print("1. Process your own text")
        print("2. View examples")
        print("3. Install clipboard support (pip install pyperclip)")
        print("4. Quit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            # Get user input
            text, prefixes = get_user_input()
            
            if text is not None and prefixes is not None:
                # Process the text
                result = add_prefixes_to_letters(text, prefixes)
                
                # Display in copyable format
                display_copyable_output(text, result, prefixes)
        
        elif choice == '2':
            # Show examples
            demonstrate_examples()
        
        elif choice == '3':
            # Provide installation instructions
            print("\n📦 To enable automatic clipboard copying:")
            print("pip install pyperclip")
            print("\nThen restart the script to use clipboard features.")
        
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()