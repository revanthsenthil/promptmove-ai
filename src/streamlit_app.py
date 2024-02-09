import streamlit as st

def main():
    st.title("Text Input App")
    
    # Get user input
    user_input = st.text_input("Enter text here:")
    
    # Display user input
    st.write("You entered:", user_input)

if __name__ == "__main__":
    main()