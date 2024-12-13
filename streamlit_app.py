import streamlit as st
from main import EmailCrew  # Import the EmailCrew class

st.title('Email Creator by Marketing.MBA')

# Set API key from secrets
os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

with st.sidebar:
    st.header('Enter Email Details')
    topic = st.text_input("Main topic:")
    targetgroup_information = st.text_area("Target Group Information:")
    key_points = st.text_area("Key Points or Specific Information Needed:")
    email_type = st.radio(
        "Select Email-Type",
        ["Content Email", "Pitch Email", "Content Email with Pitch"],
        index=0
    )

if st.button('Write Email'):
    if not topic or not targetgroup_information or not key_points or not email_type:
        st.error("Please fill all the fields.")
    else:
        with st.spinner('Creating your email...'):
            inputs = f"""
            Topic: {topic}
            Target Group: {targetgroup_information}
            Key Points: {key_points}
            Email Type: {email_type}
            """
            
            crew = EmailCrew(inputs)
            result = crew.run()
            
            st.subheader("Your Email:")
            st.write(result)
