import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["APIKey"])

if "pokedex" not in st.session_state:
    st.session_state.pokedex = {}

if "generating" not in st.session_state:
    st.session_state.generating = False

st.title("Pokedex")
st.subheader("Generate view and manage Pokemon entries")

name = st.text_input(
    "Enter Pokemon name",
    disabled=st.session_state.generating
)

col1, col2 = st.columns(2)

with col1:
    generate_clicked = st.button(
        "Generate",
        disabled=st.session_state.generating
    )

    if generate_clicked:
        if name.strip() == "":
            st.warning("Enter a Pokemon name")
        elif name in st.session_state.pokedex:
            st.warning("Already exists")
        else:
            st.session_state.generating = True
            st.rerun()

with col2:
    if len(st.session_state.pokedex) == 0:
        st.warning("No Pokedex entries yet")
    else:
        selected = st.selectbox(
            "Select a Pokemon",
            list(st.session_state.pokedex.keys()),
            disabled=st.session_state.generating
        )

        col2_a, col2_b = st.columns(2)
        
        with col2_a:
            view_clicked = st.button(
                "View Entry",
                disabled=st.session_state.generating
            )
            
        with col2_b:
            delete_clicked = st.button(
                "Delete Entry",
                disabled=st.session_state.generating
            )

        if view_clicked:
            st.text(st.session_state.pokedex[selected])
            
        if delete_clicked:
            del st.session_state.pokedex[selected]
            st.rerun()

if st.session_state.generating:
    with st.spinner("Generating Pokemon..."):
        prompt = """
Generate a full Pokedex entry with:
Name json format
4 digit ID
Stats 0-15
Description
Height
Weight
Gender
Category
Abilities
Type
Weaknesses
Evolution Line

ONLY output the entry and use the name.
NO JSON.
NO extra text.

Name: """ + name

        r = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        text = r.output[0].content[0].text
        st.session_state.pokedex[name] = text
        st.session_state.generating = False

    st.success("Pokemon generated")
    st.rerun()

    #This program uses open ai to generate a pokeimon and u can view the pokedex and there is also a delete pokedex entries that is my extra feature