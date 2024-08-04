import pandas as pd
import streamlit as st
from domain.event_from_document import EventFromDocument
from domain.google_calendar import GoogleCalendar

st.title('Loader trainning')

uploaded_file = st.file_uploader("File docx",
                                 type=['docx'],
                                 accept_multiple_files=False,
                                 key=None,
                                 help='asda')

if uploaded_file is not None:
    event = EventFromDocument(uploaded_file)
    training = event.get_events_document()



    if training is not None and len(training) != 0:
        title = st.text_input("Nombre del calendario", "Entrenamientos Redolat Team", max_chars=50)
        st.write("Puedes editar los datos del entrenamiento: ")
        df = pd.DataFrame(training)
        edited_df = st.data_editor(df)

        if st.button("Load to Calendar"):
            credentials = st.secrets['google']['credential']
            uploader = GoogleCalendar(credentials)
            title = title.strip()

            result = uploader.load_events_to_calendar(edited_df.to_records(index=False), title)

            if result:
                training = []
                st.write("Se ha cargado correctamente los entreenamientos.")
    else:
        st.warning("Hubo un problema al recuperar los datos del fichero")
