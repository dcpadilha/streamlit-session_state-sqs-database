import streamlit as st


def main():
    st.title('Welcome to this project!')
    st.markdown('This is an example about an annotation tool, that can read a message from AWS SQS Queue and annotate '
                'your avaliation on database.')


if __name__ == '__main__':
    main()
