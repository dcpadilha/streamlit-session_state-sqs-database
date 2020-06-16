# streamlit-session_state-sqs-database

This project is an example of an annotation tool. 

This is a solution example from a question that I made on [Streamlit's Forum](https://discuss.streamlit.io/t/two-people-on-same-session-state/3211). 

It receives messages from AWS SQS, load the data to be annotated, and save the annotation on database (AWS RDS).

Images from: https://www.microsoft.com/en-us/download/details.aspx?id=54765

#### Instructions

Copy the .env.sample and input your AWS informations.

To run this tool, run in a terminal:
`streamlit run main.py`