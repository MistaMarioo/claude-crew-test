# streamlit_app.py
import streamlit as st
from main import EmailCrew  # Import our custom EmailCrew class
import os  # For handling environment variables

# Set the page title
st.title('Email Creator by Marketing.MBA')

# Load the API key from Streamlit secrets and set it as an environment variable
os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
os.environ["PERPLEXITY_API_KEY"] = st.secrets["PERPLEXITY_API_KEY"]


# Create a sidebar for input fields
with st.sidebar:
    st.header('Enter Email Details')
    # Input field for the main topic
    topic = st.text_input("Main topic:")
    # Text area for target group information (allows multiple lines)
    targetgroup_information = st.text_area("Target Group Information:")
    # Text area for key points or specific information
    key_points = st.text_area("Key Points or Specific Information Needed:")
    # Radio button selection for email type
    email_type = st.radio(
        "Select Email-Type",
        ["Content Email", "Pitch Email", "Content Email with Pitch"],
        index=0  # Default selection is the first option
    )

# Create a button to trigger the email generation
if st.button('Write Email'):
    # Check if all fields are filled
    if not topic or not targetgroup_information or not key_points or not email_type:
        st.error("Please fill all the fields.")
    else:
        # Show a loading spinner while generating the email
        with st.spinner('Creating your email...'):
            # Format all inputs into a single string
            inputs = f"""
            Topic: {topic}
            Target Group: {targetgroup_information}
            Key Points: {key_points}
            Email Type: {email_type}
            """
            
            # Create an instance of EmailCrew and pass the inputs
            crew = EmailCrew(inputs)
            # Run the crew and get the result
            result = crew.run()
            
            # Display the results
            st.subheader("Your Email:")
            st.write(result)
