import streamlit as st
import google.generativeai as gemini
import PyPDF2
import re

# Streamlit app
st.title('PDF Document Chatbot with Gemini')

# Input for Gemini API Key
gemini_api_key = "AIzaSyASBgeQsfFEMjFomIUbO_5oiGdyB5yz2yE"

if gemini_api_key:
    # Set up Google API Key for Gemini
    gemini.configure(api_key=gemini_api_key)

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

    if uploaded_file is not None:
        # Read PDF file content
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        context = ""
        for page in pdf_reader.pages:
            context += page.extract_text()

        # Display PDF content (Optional: show only a preview to avoid displaying long documents)
        st.write("PDF Content Preview:")
        st.write(context[:2000] + "..." if len(context) > 2000 else context)

        # Initialize chat history in session state
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        # User input for question
        question = st.text_input("Ask a question about the document:")

        if st.button('Send'):
            if context and question:
                try:
                    # Call the Gemini model to generate the answer
                    model = gemini.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f'Answer the following question based on the document: {context}\n\nQuestion: {question}')
                    
                    # Process the response text
                    if hasattr(response, 'text'):
                        answer = response.text
                        cleaned_response = re.sub(r'\*', '', answer)

                        # Store question and answer in chat history
                        st.session_state["chat_history"].append((question, cleaned_response))
                    else:
                        st.session_state["chat_history"].append((question, "No response text found in the API response."))
                except Exception as e:
                    st.session_state["chat_history"].append((question, f"Error: {e}"))

        # Display chat history
        for i, (q, a) in enumerate(st.session_state["chat_history"]):
            st.write(f"**Q{i+1}:** {q}")
            st.write(f"**A{i+1}:** {a}")

else:
    st.warning("Please enter your Gemini API key to use Gemini features.")



hep;'';]\