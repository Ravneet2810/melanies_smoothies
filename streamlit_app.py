# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title("!Customise Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("Name on Smoothie will be", name_on_order)

#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("Your favorite fruit is:", option)

#session = get_active_session()
cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert snowpark data frame to pandas dataframe so that we can use LOC function.
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list=st.multiselect('choose up to 5 ingredients:',my_dataframe, max_selections=5)
if ingredients_list:
#    st.write(ingredients_list)
#   st.text(ingredients_list)

    ingredients_string=''
    for fruits_chosen in ingredients_list:
        ingredients_string +=fruits_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruits_chosen,' is ', search_on, '.')

        st.subheader(fruits_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruits_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)


    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
           values ('""" + ingredients_string + """','""" +name_on_order + """')"""

    st.write(my_insert_stmt)
    #st.stop()

    #if ingredients_string:
    #    session.sql(my_insert_stmt).collect()
    #    st.success('Your Smoothie is ordered!', icon="✅")

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered!', icon="✅")

