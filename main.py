import streamlit as st

import home
import annotator_tool
import session_state

PAGES = {
    "Home": home,
    "Annotation tool": annotator_tool
}

session = session_state.get(message_value=None)


def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f'Loading {selection} ...'):
        if page == annotator_tool:
            page.main(session)
        else:
            page.main()
    st.sidebar.info('This tool is an example.')


if __name__ == "__main__":
    main()
