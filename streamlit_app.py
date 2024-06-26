# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)


name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)



cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe    
#    , max_selections = 5
)

# Check the length of the selected options
if len(ingredients_list) > 5:
    st.warning('You can only select up to 5 options. Please deselect some options.')


if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
	    ingredients_string += fruit_chosen + ' '
	    
	    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
	    #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
	    
	    st.subheader(fruit_chosen + ' Nutrition Information')
	    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
	    
	    fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
	    
	    #df = pd.json_normalize(fruityvice_response)
        #st.write(fruityvice_response)
        # use the color selected to go back and get all the info from the database
        
        #table_prod_data = session.sql("select file_name, price, size_list, upsell_product_desc, file_url from catalog_for_website where color_or_style = '" + option + "';")
        #pd_df = table_prod_data.to_pandas() 

            # assign each column of the row returned to its own variable 
            family = pd_df['family'].iloc[0])+'0'
            order = pd_df['order'].iloc[0]
            calories = pd_df['nutritions.calories'].iloc[0]
            fat = pd_df['nutritions.fat'].iloc[0]
            sugar = pd_df['nutritions.sugar'].iloc[0]
            carbohydrates = pd_df['nutritions.carbohydrates'].iloc[0]
            protein = pd_df['nutritions.protein'].iloc[0]

        # display the info on the page
            st.markdown('**Family:** '+ family)
            st.markdown('**Order:** ' + order)
            st.markdown('**Calories:** ' + nutritions.calories)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
	
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
