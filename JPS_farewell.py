import streamlit as st
import base64
from PIL import Image
# from pathlib import Path

#### Wordcloud
# from os import path
import numpy as np
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud, STOPWORDS

import pandas as pd


st.set_page_config(
    page_title="JPS farewell to Naz",
    page_icon=(":tada:"),
    layout="wide",
    # initial_sidebar_state="auto",
)

@st.experimental_memo#@st.cache()
def get_jps_messages():
    jps_survey = pd.read_excel("Farewell message to Khairul Nazran.xlsx")


    #### JPS messages
    survey_cols = jps_survey.columns
    jps_survey[survey_cols[7]] = jps_survey[survey_cols[7]].fillna("Anonymous")
    jps_messages = jps_survey.set_index(survey_cols[6]).to_dict()[survey_cols[7]]

    #### One word adjectives
    jps_survey[survey_cols[5]] = jps_survey[survey_cols[5]].str.replace("Serious but Not Serious","Serious_but_not_serious")
    jps_survey[survey_cols[5]] = jps_survey[survey_cols[5]].str.replace("(one word not enough ;p)",'')
    jps_survey[survey_cols[5]] = jps_survey[survey_cols[5]].str.replace("(Is there no problem he can’t fix)",'No_problem_he_cant_fix')
    jps_survey[survey_cols[5]] = jps_survey[survey_cols[5]].str.replace("Nice person",'Nice')

    jps_survey[survey_cols[5]] = jps_survey[survey_cols[5]].str.replace("?",'',regex=False)
    jps_survey[survey_cols[5]] = jps_survey[survey_cols[5]].str.replace("(",'',regex=False)
    jps_survey[survey_cols[5]] = jps_survey[survey_cols[5]].str.replace(")",'',regex=False)
    jps_survey[survey_cols[5]] = jps_survey[survey_cols[5]].str.title().str.strip()
    wordcloud_adjectives = ' '.join(jps_survey[survey_cols[5]].fillna(''))


    return jps_messages, wordcloud_adjectives


def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

@st.experimental_memo#@st.cache()
def get_wordcloud(text):
    naz_mask = np.array(Image.open("pic/naz-removebg-preview.png"))

    stopwords = set(STOPWORDS)
    stopwords.add("said")

    # generate word cloud
    wc = WordCloud(background_color="black", max_words=2000, mask=naz_mask,
                stopwords=stopwords, contour_width=0.8, contour_color='steelblue',width=1600, height=800).generate(text)

    return wc
jps_messages, wordcloud_adjectives = get_jps_messages()


def page_content(page_number):
    if page_number == 0:
        cols = st.columns([0.7,1.2,1])

        with cols[1]:
            # st.header("Congratulations! and goodbye...")
            st.write(
                f"""<span style="color:#00FFFF;font-size:26px"> <b> Congratulations! and goodbye... <br>to the Meme Master</b></span>""",
                unsafe_allow_html=True,
            )

            st.subheader("The Usual Naz... :male-office-worker:")
            naz_office = Image.open('naz_photos/naz_office.jpg')
            st.image(naz_office, width=455)
            naz_pp = Image.open('naz_photos/naz.png')
            st.image(naz_pp, width=380)

            # st.write("<br>",unsafe_allow_html=True)
            st.write("<br>",unsafe_allow_html=True)


            st.subheader("Naz after October 4th 2021... :tada: ")
            # st.write(
            #     f"""<p><img src="https://media3.giphy.com/media/6nuiJjOOQBBn2/200w.webp?cid=ecf05e47xcmnv9n8vasc1d01665fpyw6u8qee6tg305wyews&rid=200w.webp&ct=g" style="width:500px;height:450px;"></p>""",
            #     unsafe_allow_html=True,
            # )  #### Requires internet
            file_ = open('messages/celebration.gif', "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()

            st.write(
                f"""<p><img src="data:image/gif;base64,{data_url}" style="width:500px;height:400px"></p>""",
                unsafe_allow_html=True,
            )
            st.write("\n")

    elif page_number == 1:
        st.header("In JPS-ians' memory, You're always... :sunglasses:")
        #### Change text here
        text = wordcloud_adjectives

        wc = get_wordcloud(text)
        # show
        fig = plt.figure(figsize=[20, 10], facecolor='k')
        # plt.imshow(wc, interpolation='bilinear')
        plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
                interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout(pad=0)

        wc_cols = st.columns([0.7,1,0.7])
        with wc_cols[1]:
            st.pyplot(fig)

    elif page_number == 2:
        st.header("""Messages from your fellow JPS-ians! :man-woman-girl-boy:""")
        st.write("<br>",unsafe_allow_html=True)
        st.write("<br>",unsafe_allow_html=True)
        # st.write(jps_messages)
        count = 0
        for message, people in jps_messages.items():
            if people == 'Li Ming':
                cols_to_write = st.columns ([1,6,1.5])
                cols_to_write[1].write(
                    f"""<span style="font-size:17px;color:#FFCC66"> {message.strip()}</span> <span style="color:#FFC0CB;font-size:19px;text-align:right"> - <b><i>{people}</i></b></span>""",
                    unsafe_allow_html=True,
                )
                # cols_to_write[1].write(
                #     f""" <p style="color:#FFC0CB;font-size:28px;text-align:right"> - <b><i>{people}</i></b></p>""",
                #     unsafe_allow_html=True,
                # )
        st.write("<br>",unsafe_allow_html=True)
        st.write("<br>",unsafe_allow_html=True)
        for message, people in jps_messages.items():
            if people != 'Li Ming':
                cols_to_write = st.columns([1,3,3,1.5])
                if count % 2 == 0:
                    col_picked = 1
                    # cols_to_write[col_picked].write(
                    #     f"""<p style="font-size:20px;"> {message.strip()}</p>""",
                    #     unsafe_allow_html=True,
                    # )
                    # cols_to_write[col_picked].write(
                    #     f""" <p style="color:#FFC0CB;font-size:20px;text-align:right"> - <b>{people}</b></p>""",
                    #     unsafe_allow_html=True,
                    # )
                else:
                    col_picked = 2
                    # cols_to_write[col_picked].write(
                    #     f"""<p style="font-size:20px;text-align:right"> {message.strip()}</p>""",
                    #     unsafe_allow_html=True,
                    # )
                    # cols_to_write[col_picked].write(
                    #     f""" <p style="color:#FFC0CB;font-size:20px;text-align:right"> - <b>{people}</b></p>""",
                    #     unsafe_allow_html=True,
                    # )
                cols_to_write[col_picked].write(
                    f"""<span style="font-size:15px"> {message.strip()}</span>  -  <span style="color:#FFC0CB;font-size:15px"> <b><i>{people}</i></b></span>""",
                    unsafe_allow_html=True,
                )

                count +=1

    elif page_number == 3:
        st.header("Unable to meet because of MCO... but we still have these!")

        #### Naz general photos
        cols = st.columns([2,1.7,2])
        naz_office = Image.open('naz_photos/ili_party.jpeg')
        cols[0].image(naz_office, width=380)
        naz_pp = Image.open('naz_photos/naz.png')
        cols[1].image(naz_pp, width=300)
        gsy4 = Image.open('naz_photos/Hackathon win with Naz.jpeg')
        cols[2].image(gsy4, width=350)


        #### DSA
        cols = st.columns([1.7,2.7])
        naz_flower = Image.open('naz_photos/naz_flower.png')
        cols[0].image(naz_flower, width=400)
        dsa_flower = Image.open('naz_photos/dsa_flower.png')
        cols[1].image(dsa_flower, width=700)
        #### With GSY
        cols = st.columns([1,1,1])
        gsy1 = Image.open('naz_photos/gsy1.jpeg')
        cols[0].image(gsy1, width=350)
        gsy2 = Image.open('naz_photos/gsy2.jpeg')
        cols[1].image(gsy2, width=350)
        gsy3 = Image.open('naz_photos/gsy3.jpeg')
        cols[2].image(gsy3, width=350)
        # gsy4 = Image.open('naz_photos/gsy4.jpeg')
        # cols[3].image(gsy4, width=400)

        st.write('\n\n')
        st.write(
            f"""<p style="text-align:right;color:#FFCC66;font-size:50px"> <b><i> Good Luck in Your Future Endeavors!</b></i></p>""",
            unsafe_allow_html=True,
        )

if 'page_num' not in st.session_state:
    st.session_state['page_num'] = 0
    page_content(st.session_state['page_num'])

# st.write(st.session_state.page_num)
# st.write(st.session_state)

def previous_page():
    st.balloons()
    st.session_state['page_num'] -= 1
    page_content(st.session_state['page_num'])


def next_page():
    st.balloons()
    st.session_state['page_num'] += 1
    page_content(st.session_state['page_num'])

cols = st.columns([8,1])
with cols[0]:
    if st.session_state['page_num'] != 0:  
        st.button("Previous", on_click=previous_page)

with cols[1]:
    if st.session_state['page_num'] != 3:
        st.button("Next", on_click=next_page)
