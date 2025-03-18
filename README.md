# AI-DOCUMENTATION

The application allows users to upload a ZIP file containing source code or directly paste code into a text area. It then uses the Google Gemini API to generate documentation, including an analysis of the code's workflow and relationships between modules, function descriptions, parameter details, and examples. The generated documentation is displayed in the Streamlit app and can be downloaded as a text file. The application handles large codebases by splitting them into smaller chunks before sending them to the API.
