import streamlit as st
import networkx as nx
import pandas as pd
import operator

#ndlib imports----------
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
from ndlib.viz.bokeh.MultiPlot import MultiPlot
from bokeh.io import export_png
from bokeh.io import output_notebook,show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

import streamlit.components.v1 as components  # Import Streamlit



def main():
    st.title("Model-Based Learning of Information Diffusion in Social Networks for Twitter Dataset")
    #st.subheader("Select a topic which you'd like to get the sentiment analysis on :")
    
    df = pd.read_csv("Centrality.csv")
    st.sidebar.subheader("Data of Top 10 Nodes based on Centrality")
    st.sidebar.table(df)
    
   # infected_node = str(st.text_input("Enter the user you are interested in (Press Enter once done)")) 
    
    infected_node = st.sidebar.selectbox("Select Node",("838136759254978562","352612489","526439855","1951228699","1455485081594777612","761584018823479298","1160502001249280000","479333563","1070332391217078273","915246066869719041"))
 
    diffusion_model_1 = st.sidebar.selectbox("Select Model 1",("SIS","SIR","SI"))
    diffusion_model_2 = st.sidebar.selectbox("Select Model 2",("SIS","SIR","SI"))

    
    
    iterations = st.sidebar.slider("iterations",1,1000)
    
#     st.sidebar.header("About App")
#     st.sidebar.info("A Twitter Sentiment analysis Project which will scrap twitter for the topic selected by the user. The extracted tweets will then be used to determine the Sentiments of those tweets. \
#                     The different Visualizations will help us get a feel of the overall mood of the people on Twitter regarding the topic we select.")
#     st.sidebar.text("Built with Streamlit")
#     st.sidebar.text("Created By Abijeeth Vasra")
    
#     st.sidebar.header("For Any Queries/Suggestions Please reach out at :")
#     st.sidebar.info("vasraabijeeth@gmail.com")

    def selected_model_1():
        if(diffusion_model_1 == "SIS"):
            SIS(infected_node,iterations,"1")
        if(diffusion_model_1 == "SIR"):
            SIR(infected_node,iterations,"1")
        if(diffusion_model_1 == "SI"):
            SI(infected_node,iterations,"1")
            
    def selected_model_2():
        if(diffusion_model_2 == "SIS"):
            SIS(infected_node,iterations,"2")
        if(diffusion_model_2 == "SIR"):
            print("SIR called");
            SIR(infected_node,iterations,"2")
        if(diffusion_model_1 == "SI"):
            SI(infected_node,iterations,"2")

 
    
    def display_image():
        image1 = Image.open("bokeh_plot_1.png")
        image2 = Image.open("bokeh_plot_2.png")
        st.image([image1,image2])
        
    

    
    def SIS(infected_node,iterations,z):
        infected_node = int(infected_node)
        print(type(infected_node))
       
        vm=MultiPlot()
    
        df=pd.read_csv('data.csv')
        print("data.csv fetched")

        #G=nx.from_pandas_edgelist(df,create_using=nx.DiGraph())
        G= nx.from_pandas_edgelist(df,source='source',target='target', create_using=nx.DiGraph())
        print("G done")

        model=ep.SISModel(G)
        config=mc.Configuration()
        #supply the top 10 infected nodes of all 3 centralities 1 by 1 

        #infected_nodes=sorted_x

        config.add_model_parameter("beta",0.01) #infection rate
        config.add_model_parameter("lambda",0.005) #recovery rate
        config.add_model_parameter("fraction_infected",0.05)

        config.add_model_initial_configuration("Infected",[infected_node]) #setting initial infection node
        print("Config over and inf set")

        model.set_initial_status(config)
        iterations=model.iteration_bunch(iterations)
        print(model.get_info())

        trends=model.build_trends(iterations)
        #diffusion trend
        p1=DiffusionTrend(model,trends).plot(width=400,height=400)

        vm.add_plot(p1)
        m=vm.plot()
        output_notebook()
       
       #st.pyplot(m)
        show(m)
        if(z == "1"):
            export_png(m, filename = "bokeh_plot_1.png")
            
        elif(z == "2"):
            export_png(m, filename = "bokeh_plot_2.png")
           
       


    def SIR(infected_node,iterations,y):
        infected_node = int(infected_node)
        vm=MultiPlot()

        df=pd.read_csv('data.csv')

        #G=nx.from_pandas_edgelist(df,create_using=nx.DiGraph())
        G= nx.from_pandas_edgelist(df,source='source',target='target', create_using=nx.DiGraph())

        model=ep.SIRModel(G)
        config=mc.Configuration()
        #supply the top 10 infected nodes of all 3 centralities 1 by 1 


        config.add_model_parameter("beta",0.05)
        config.add_model_parameter("gamma",0.01)
        config.add_model_parameter("fraction_infected",0.05)

        config.add_model_initial_configuration("Infected",[infected_node])


        model.set_initial_status(config)
        iterations=model.iteration_bunch(iterations)
        print(model.get_info())

        trends=model.build_trends(iterations)
        #diffusion trend
        p1=DiffusionTrend(model,trends).plot(width=400,height=400)

        vm.add_plot(p1)

        m=vm.plot()
        output_notebook()
        show(m)
        if(y == "1"):
            print("correct2");
            export_png(m, filename = "bokeh_plot_1.png")
           
        elif(y == "2"):
            print("correct2");
            export_png(m, filename = "bokeh_plot_2.png")

    def SI(infected_node,iterations,r):
        infected_node = int(infected_node)
        vm=MultiPlot()

        df=pd.read_csv('data.csv')

        #G=nx.from_pandas_edgelist(df,create_using=nx.DiGraph())
        G= nx.from_pandas_edgelist(df,source='source',target='target', create_using=nx.DiGraph())

        model=ep.SIModel(G)
        config=mc.Configuration()
        #supply the top 10 infected nodes of all 3 centralities 1 by 1 


        config.add_model_parameter("beta",0.05)
        config.add_model_parameter("gamma",0.01)
        config.add_model_parameter("fraction_infected",0.05)

        config.add_model_initial_configuration("Infected",[infected_node])


        model.set_initial_status(config)
        iterations=model.iteration_bunch(iterations)
        print(model.get_info())

        trends=model.build_trends(iterations)
        #diffusion trend
        p1=DiffusionTrend(model,trends).plot(width=400,height=400)

        vm.add_plot(p1)

        m=vm.plot()
        output_notebook()
        show(m)
        if(r == "1"):
            print("correctSI");
            export_png(m, filename = "bokeh_plot_1.png")
           
        elif(r == "2"):
            print("correctSI");
            export_png(m, filename = "bokeh_plot_2.png")
            
    def compare_models():
        selected_model_1()
        selected_model_2()
           
    st.sidebar.button("Compare",key=None, help=None, on_click=compare_models())
   
    # Render the h1 block, contained in a frame of size 200x200.
    
   
    #components.html("<html><body><iframe src="https://public.flourish.studio/visualisation/13002944/" height="200" width="300" title="Iframe Example"></iframe></body></html>", width=200, height=200)
    #components.iframe("https://public.flourish.studio/visualisation/13002944/",height="600")
    st.write("Graphical Network of fetched User")
    components.html(
    """
    <iframe src='https://flo.uri.sh/visualisation/13002944/embed' title='Interactive or visual content' class='flourish-embed-iframe' frameborder='0' scrolling='no' style='width:100%;height:600px;' sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation'></iframe><div style='width:100%!;margin-top:4px!important;text-align:right!important;'><a class='flourish-credit' href='https://public.flourish.studio/visualisation/13002944/?utm_source=embed&utm_campaign=visualisation/13002944' target='_top' style='text-decoration:none!important'><img alt='Made with Flourish' src='https://public.flourish.studio/resources/made_with_flourish.svg' style='width:105px!important;height:16px!important;border:none!important;margin:0!important;'> </a></div>
    """,
    height=600,
)
    st.subheader("Comparison")
    st.write("Selected Node ID = ",infected_node)
    st.write("Model 1 = ",diffusion_model_1)
    st.write("Model 2 = ",diffusion_model_2)
    display_image()
    
   
if __name__ == '__main__':
    main()