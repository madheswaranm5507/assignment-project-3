import streamlit as st
from streamlit_option_menu import option_menu
import pymongo
import pandas as pd
pd.set_option('display.max_columns', None)
import plotly.express as px
from PIL import Image
import warnings
warnings.filterwarnings("ignore")
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go


st.set_page_config(layout="wide")
st.title(":red[AIRBNB DATA ANALYSIS]")

def dataframe():
    df = pd.read_csv(r"C:\Users\madhe\OneDrive\Desktop\Airbnb Analysis\airbnb_data.csv")
    return df

df = dataframe()

with st.sidebar:
    select = option_menu("AIRBNB ANALYSIS",["Home","Data Visualization and Exploration"])

if select == "Home":

    st.header("Introduction")
    st.write("""Airbnb is an online marketplace that connects people who want to rent out their property with people who are looking for accommodations, 
                typically for short stays. Airbnb offers hosts a relatively easy way to earn some income from their property. 
                Airbnb company was founded in 2008 when two Hosts welcomed three guests to their
                San Francisco home, and has since grown to over 4 million Hosts who have
                welcomed over 1.5 billion guest arrivals in almost every country across the globe.
                Airbnb is headquartered in San Francisco, California, the US.""")
    
    st.header("Technologies Used")
    st.write("1) Python - The project is implemented using the Python programming language.")
    st.write("2) MongoDB - Retrieve the Airbnb dataset in the MongoDB database for efficient data management.")
    st.write("3) Plotly - Plotly is a powerful Python library used for creating interactive data and visualizations.")
    st.write("4) Pandas - A Powerfull data manipulation in pandas. providing functionalities such as data filtering, dataframe create, transformation, and aggregation.")
    st.write("5) Streamlit - The user interface and visualization are created using the Streamlit framework.")
    


if select == "Data Visualization and Exploration":

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Geospatial Visualization","Price Analysis and Visualization","Availability Analysis by Season","Location Based Insights", "Interactive Visualization"])

    with tab1:
        st.title("Geospatial Visualization")
        fig_1 = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="price", size= "accommodates",
                                  color_continuous_scale="rainbow",hover_name="name",hover_data="review_scores", range_color=(0,50000), mapbox_style="carto-positron",
                                  zoom=2,width= 1200, height= 900)
        st.plotly_chart(fig_1)


    with tab2:
        st.title("Price Analysis and Visualization")
        
        country = st.selectbox("Select The Country" , df["country"].unique())
        df1 = df[df["country"] == country]
        df1.reset_index(drop= True, inplace= True)
        
        room_type = st.selectbox("Select The Room Type",df1["room_type"].unique())
        df2 = df1[df1["room_type"] == room_type]
        df2.reset_index(drop= True, inplace= True)

        df_bar =pd.DataFrame(df2.groupby("property_type")[["price","review_scores","number_of_reviews"]].sum())
        df_bar.reset_index(inplace=True)

        col1,col2 = st.columns(2)
        with col1:
            fig_bar = px.bar(df_bar, x ="property_type", y="price",hover_data=["review_scores","number_of_reviews"], title="PRICE FOR PROPERTY TYPES",
                            color_discrete_sequence=px.colors.sequential.Burg_r,width=500,height=450)                 
            st.plotly_chart(fig_bar)  

        with col2:
            property_type = st.selectbox("Select The Property Type", df2["property_type"].unique())
            df3 = df2[df2["property_type"] == property_type]
            df3.reset_index(drop=True,inplace=True)

            df_pie = pd.DataFrame(df3.groupby("host_response_time")[["price","bedrooms"]].sum())
            df_pie.reset_index(inplace=True)
            
            fig_pie = px.pie(df_pie, values="price", names= "host_response_time",hover_data="bedrooms",color_discrete_sequence=px.colors.sequential.Rainbow_r,
                            title= "PRICE DIFFERENCE BASED ON THE HOST RESPONCE TIME",width=500,height=450)
            st.plotly_chart(fig_pie)


        host_response_type = st.selectbox("Select The Host Response Time",df3["host_response_time"].unique())
        df4 = df3[df3["host_response_time"] == host_response_type]  

        df_bar_host = pd.DataFrame(df4.groupby("bed_type")[["price","minimum_nights","maximum_nights"]].sum())
        df_bar_host.reset_index(inplace=True)
        
        col1,col2 = st.columns(2)
        with col1:
            fig_bar_host = px.bar(df_bar_host, x= "price", y="bed_type",title="PRICE ANALYSIS FOR MINIMUM NIGHTS AND MAXIMUM NIGHTS",
                        hover_data=["minimum_nights","maximum_nights"],barmode="group",color_discrete_sequence=px.colors.sequential.Rainbow,width=500,height=450)
            st.plotly_chart(fig_bar_host)


        df_bar_host_2 = pd.DataFrame(df4.groupby("bed_type")[["price","bedrooms","beds","accommodates"]].sum())
        df_bar_host_2.reset_index(inplace=True)

        with col2:
            fig_bar_host = px.bar(df_bar_host_2, x= "price", y="bed_type",title="PRICE ANALYSIS FOR BEDROOMS, BEDS, ACCOMMODATES",
                            hover_data=["bedrooms","beds","accommodates"],barmode="group",color_discrete_sequence=px.colors.sequential.Rainbow_r,width=500,height=450)

            st.plotly_chart(fig_bar_host)


    with tab3:
        st.title("Availability Analysis by Season") 

        country_Availability_Analysis = st.selectbox("Select The Country Availability Analysis",df["country"].unique())     
        df1_a = df[df["country"] == country_Availability_Analysis]
        df1_a.reset_index(drop = True,inplace=True)

        property_type_Availability_Analysis = st.selectbox("Select The property type Availability Analysis",df1_a["property_type"].unique())
        df2_a = df1_a[df1_a["property_type"] == property_type_Availability_Analysis]
        df2_a.reset_index(drop=True,inplace=True)
        
        col1,col2 = st.columns(2)
        with col1:
            df_a_availability_30 = px.sunburst(df2_a, path = ["room_type","bed_type","is_location_exact"],values="availability_30",width=600,height=500,title="Available for Booking the Next 30 days",
                                    color_discrete_sequence= px.colors.sequential.Bluered_r)
            
            st.plotly_chart(df_a_availability_30)
        with col2:
            df_a_availability_60 = px.sunburst(df2_a, path = ["room_type","bed_type","is_location_exact"],values="availability_60",width=600,height=500,title="Available for Booking the Next 60 days",
                            color_discrete_sequence= px.colors.sequential.Aggrnyl_r)

            st.plotly_chart(df_a_availability_60)

        col1,col2 = st.columns(2)
        with col1:
            df_a_availability_90 = px.sunburst(df2_a, path = ["room_type","bed_type","is_location_exact"],values="availability_90",width=600,height=500,title="Available for Booking the Next 90 days",
                        color_discrete_sequence= px.colors.sequential.Darkmint_r)

            st.plotly_chart(df_a_availability_90)
        with col2:
            df_a_availability_365 = px.sunburst(df2_a, path = ["room_type","bed_type","is_location_exact"],values="availability_365",width=600,height=500,title="Available for Booking the Next 365 days",
                    color_discrete_sequence= px.colors.sequential.Greens_r)

            st.plotly_chart(df_a_availability_365)    


        Room_type_Availability_Analysis = st.selectbox("Select The Room Type Availability Analysis",df2_a["room_type"].unique()) 
        df3_a = df2_a[df2_a["room_type"] == Room_type_Availability_Analysis]
        df3_a.reset_index(drop=True,inplace=True) 

        df_ta_bar = df3_a.groupby("host_location")[["price","availability_30","availability_60","availability_90","availability_365"]].sum()
        df_ta_bar.reset_index(inplace=True)

        fig_df_ta_bar = px.bar(df_ta_bar, x = "price", y ="host_location" ,
                               title="AVAILABILITY BASED ON THE HOST LOCATION",hover_data=["availability_30","availability_60","availability_90","availability_365"],barmode="group",color_discrete_sequence=px.colors.sequential.Rainbow_r,width=1400,height=800)
        
        st.plotly_chart(fig_df_ta_bar)


    with tab4:
        st.title("Location Based Insights")

        country_Location_Analysis = st.selectbox("Select The Country Location Analysis",df["country"].unique())
        df1_l = df[df["country"] == country_Location_Analysis]
        df1_l.reset_index(drop=True,inplace= True)

        Property_type_Location_Analysis = st.selectbox("Select The Property Type Location Analysis",df1_l["property_type"].unique())
        df2_l = df1_l[df1_l["property_type"] == Property_type_Location_Analysis]
        df2_l.reset_index(drop=True, inplace=True)
        
        accommodates_Location_Analysis = df2_l.groupby("accommodates")[["bedrooms","beds","extra_people","cleaning_fee"]].sum()
        accommodates_Location_Analysis.reset_index(inplace=True)   

        fig_1= px.bar(accommodates_Location_Analysis, x="accommodates", y= ["cleaning_fee","bedrooms","beds"], title="LOCATION ANALYSIS FOR ACCOMMODATES",
                    hover_data= "extra_people", barmode='group', color_discrete_sequence=px.colors.sequential.Rainbow_r,width=1000,height=600)
        st.plotly_chart(fig_1)
        

        Room_type_Location_Analysis = st.selectbox("Select The Room Type Location Analysis", df2_l["room_type"].unique())
        df3_l = df2_l[df2_l["room_type"] == Room_type_Location_Analysis]
        df3_l.reset_index(drop=True,inplace=True)

        
        fig_2 = px.bar(df3_l, x =["street","host_location","host_neighbourhood"], y="market",hover_data=["market","host_name","name"],title="LOCATION ANALYSIS FOR MARKET",
                       color_discrete_sequence=px.colors.sequential.Rainbow_r,width=1000,orientation="h",barmode="group"
               )
        
        st.plotly_chart(fig_2)

        fig_3 = px.bar(df3_l, x =["host_neighbourhood","cancellation_policy"], y="government_area",hover_data=["government_area","guests_included"],title="LOCATION ANALYSIS FOR GOVERNMENT AREA",
                color_discrete_sequence=px.colors.sequential.Greens_r,width=1000,orientation="h",barmode="group"
        )
        
        st.plotly_chart(fig_3)


    with tab5:
        st.title("Interactive Visualization")

        country_i = st.selectbox("Select The Country_i",df["country"].unique())
        df1_i = df[df["country"] == country_i]
        df1_i.reset_index(drop=True,inplace=True)

        property_type_i = st.selectbox("Select The Property Type_i",df1_i["property_type"].unique())
        df2_i = df1_i[df1_i["property_type"] == property_type_i]
        df2_i.reset_index(drop=True,inplace=True)

        df2_i_sorted = df2_i.sort_values(by="price")
        df2_i_sorted.reset_index(drop=True,inplace=True)

        df_price_i =pd.DataFrame(df2_i_sorted.groupby("host_neighbourhood")["price"].agg(["sum","mean"]))
        df_price_i.reset_index(inplace= True)
        df_price_i.columns = ["Host neighbourhood", "Total Price" , "Avarage Price"]

        col1,col2 = st.columns(2)
        with col1:
            fig_price_1 = px.bar(df_price_i, x= "Total Price", y ="Host neighbourhood",title="PRICE BASED ON THE HOST NEIGHBOURHOOD",
                        orientation="h",width=700,height=600)
            st.plotly_chart(fig_price_1)
        with col2:
            fig_price_2 = px.bar(df_price_i, x= "Avarage Price", y ="Host neighbourhood",title="AVERAGE PRICE BASED ON THE HOST NEIGHBOURHOOD",
                        orientation="h",width=700,height=600)
            st.plotly_chart(fig_price_2)


        df_price_2 =pd.DataFrame(df2_i_sorted.groupby("host_location")["price"].agg(["sum","mean"]))
        df_price_2.reset_index(inplace=True)
        df_price_2.columns = ["Host Location", "Total Price", "Avarage Price"]   

        col1,col2 = st.columns(2)
        with col1:
            fig_price_3 = px.bar(df_price_2, x= "Total Price", y ="Host Location",title="PRICE BASED ON THE HOST LOCATION",
                        orientation="h",width=700,height=600,color_discrete_sequence=px.colors.sequential.PuBuGn_r)
            st.plotly_chart(fig_price_3)
        with col2:
            fig_price_4 = px.bar(df_price_2, x= "Avarage Price", y ="Host Location",title="AVERAGE PRICE BASED ON THE HOST LOCATION",
                        orientation="h",width=700,height=600,color_discrete_sequence=px.colors.sequential.PuBuGn_r)
            st.plotly_chart(fig_price_4) 

        Room_type_i = st.selectbox("Select The Room Type_i",df2_i_sorted["room_type"].unique()) 
        df3_i = df2_i_sorted[df2_i_sorted["room_type"] == Room_type_i]
        df3_i.reset_index(drop=True,inplace=True) 

        df3_i_sorted_price = df3_i.sort_values(by = "price")
        df3_top_100_price = df3_i_sorted_price.head(100)
        
        col1,col2 = st.columns(2)
        with col1:
            fig_top_100_price_1 = px.bar(df3_top_100_price, x="name",y="price",color="price",color_continuous_scale="rainbow",
                                        range_color=(0,df3_top_100_price["price"].max()),hover_data=["minimum_nights","maximum_nights","accommodates"],
                                        title="TOP 100$ PRICE IN - MINIMUM_NIGHTS MAXIMUM_NIGHT AND ACCOMMODATES",width=600,height=500) 
            
            st.plotly_chart(fig_top_100_price_1)
        with col2:
            fig_top_100_price_2 = px.bar(df3_top_100_price, x="name",y="price",color="price",color_continuous_scale="rainbow",
                                        range_color=(0,df3_top_100_price["price"].max()),hover_data=["accommodates","bedrooms","bed_type","beds"],
                                        title="TOP 100$ PRICE IN - BEDROOMS, BEDS, BED_TYPE AND ACCOMMODATES",width=600,height=500) 
            
            st.plotly_chart(fig_top_100_price_2)






        