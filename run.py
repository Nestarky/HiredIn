import streamlit as st
import numpy as np
from time import sleep

from Drivers import *
from Scraper import *


if ("session" not in st.session_state):
    st.session_state.session = LinkedIn(WebDriver= 'Firefox')

left, middle, right = st.columns(spec= 3)
middle.image(image= r"./Logo.png")

@st.dialog(title= "Preview", width= "large")
def preview_and_save():
    placeholder = st.empty()
    with placeholder.container():
        st.write("#### Fetching...")
        sleep(1)
    with placeholder.container():
        st.write("#### Scroll down to save the preview as CSV")
        result = st.session_state.session.search(job, location)
        csv = result.to_csv()
        result.index = np.arange(1, len(result) + 1)
        st.table(result.loc[: , ["Job Title" , "Company" , "Location" , "List Date"]])
        st.download_button(
            label= 'Save As CSV',
            data= csv,
            file_name= f"{job} in {location}.csv",
            width= 'stretch'
        )

with st.container(border= True):
    form_left, form_right = st.columns(
        spec= [0.2, 0.7],
        vertical_alignment= "center"
    )
    form_left.write("### Job")
    job = form_right.text_input(
        label= "job",
        label_visibility= "collapsed"
    )
    form_left.write("### Location")
    location = form_right.text_input(
        label= "Location",
        value= "United States",
        label_visibility= "collapsed",
        placeholder= "United States"
    )

    st.button(
        label= "Fetch it",
        width= 'stretch',
        on_click= preview_and_save
    )

