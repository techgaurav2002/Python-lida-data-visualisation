import streamlit as st
from lida import Manager,TextGenerationConfig,llm
from dotenv import load_dotenv
import os
import openai
import io
from PIL import Image
from io import BytesIO
import base64


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def base64_to_image(base64_string):
    #decode the base 64 string
    byte_data = base64.b64decode(base64_string)
    #use byteId to convert the byte data to image
    return Image.open(BytesIO(byte_data))

lida = Manager(text_gen = llm("openai"))
textgen_config = TextGenerationConfig(n=1,temperature=0.5,model="gpt-3.5-turbo",use_cache=True)

menu = st.sidebar.selectbox("Chose an option",["summarize","Question based Graph"])

if menu == "summarize":
    st.subheader("Summerization of your data")
    file_uploader = st.file_uploader("upload your file",type='csv')
    if file_uploader is not None:
        path_to_save = "filename.csv"
        with open(path_to_save,"wb") as f:
            f.write(file_uploader.getvalue())
        summary = lida.summarize("filename.csv",summary_method="default",textgen_config=textgen_config)
        st.write(summary)
        goals = lida.goals(summary,n=5,textgen_config=textgen_config)
        for goal in goals:
            st.write(goal)
        i = 0
        library = "seaborn"
        textgen_config = TextGenerationConfig(n=2,temperature=0.2,use_cache=True)
        charts = lida.visualize(summary=summary,goal=goals[i],textgen_config=textgen_config,library=library)
        img_base64_string = charts[0].raster
        img = base64_to_image(img_base64_string)
        st.image(img)
elif menu == "Question based Graph":
    st.subheader("Query your data to generate Graph")
    file_uploader = st.file_uploader("upload your CSV",type='csv')
    if file_uploader is not None:
        path_to_save = "filename1.csv"
        with open(path_to_save,"wb") as f:
            f.write(file_uploader.getvalue())

        text_area = st.text_area("Query your data to generate Graph",height=200)
        if st.button("Generate Graph"):
            if len(text_area)>0:
                st.info("your query: " + text_area)
                lida = Manager(text_gen = llm("openai"))
                textgen_config = TextGenerationConfig(n=2,temperature=0.2,use_cache=True)
                summary = lida.summarize("filename1.csv",summary_method="default",textgen_config=textgen_config)
                library = "seaborn"
                user_query = text_area
                charts = lida.visualize(summary=summary,goal=user_query,textgen_config=textgen_config,library=library)
                charts[0]
                # explanations = lida.explain(code=code, library=library, textgen_config=textgen_config) 
                # for row in explanations[0]:
                #     print(row["section"]," ** ", row["explanation"])
                image_base64 = charts[0].raster
                img = base64_to_image(image_base64)
                st.image(img)
