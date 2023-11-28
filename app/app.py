import streamlit as st
import numpy as np 
from styles import footnote, sidebar, hide_streamlit_style
from utils_app import get_plot, generate_dataframe, get_parallel_coodi, get_z_value, get_box_plot
from genetic_alg import genetic_algorithm
import plotly.express as px
import json 
import logging 
import pandas as pd  
 
STEP = 0.15
CXPB = 0.2
MUTPB = 0.5

f = open('app/options.json', "r")
options = json.loads(f.read())
    
def main():
    
    
    st.set_page_config(
        page_title="Genetic algorithms",
        page_icon=":bar_chart:",
        initial_sidebar_state="expanded"
        )

    if "processed_output" not in st.session_state:
        st.session_state['processed_output'] = []
    
    if "df_results" not in st.session_state:
        st.session_state['df_results'] = pd.DataFrame([])
        
    if "disabled_btn" not in st.session_state:
        st.session_state['disabled_btn'] = True
    
    if "id" not in st.session_state:
        st.session_state['id'] = ""
    
    if "output" not in st.session_state:
        st.session_state["output"] = False
    
    # st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.write(footnote, unsafe_allow_html=True)
    st.title('Testing GA for optimization')
    
    np.random.seed(100)
    st.markdown(sidebar, unsafe_allow_html=True)
    st.sidebar.title("Parameters")
    
    min_max_x = st.sidebar.slider("Min Max X Value:", -5.0, 5.0, (-2.0, 2.0), step=STEP)
    min_max_y = st.sidebar.slider("Min Max Y Value:", -5.0, 5.0, (-2.0, 2.0), step=STEP)
    population_size = st.sidebar.number_input("Population Size:", value=20) 
    num_bests = population_size 
    ngen = st.sidebar.number_input("Number of Generations:", value=3) 
    option = st.selectbox('Which function do you want to optimize?', list(options.keys()))
    
    opt_type = st.sidebar.radio("Type of optimization:", ["Minimization", "Maximization"], )
    if opt_type == "Minimization":
        minimize = True
    else: 
        minimize = False
    col1, col2 = st.sidebar.columns([1,1])
    
    # submit = st.button('Generate Graph')
    tab1, tab2, tab3 = st.tabs(["Graph", "Parameters", "Results"])
    
    with tab1:
        submit = st.button('Generate Graph')
        if submit:
            st.write("3D Plot of the function: ", option)
            fig, st.session_state['id'] = get_plot(option, options, min_max_x, min_max_y, STEP)
            st.plotly_chart(fig)
            st.session_state['disabled_btn'] = False
            
    clear_btn = col2.button('Clear', disabled=st.session_state['disabled_btn'])
    run_script_btn = col1.button("Run Script", type="primary", disabled=st.session_state['disabled_btn'])
        
    
    with tab2:
        st.write("Min Max X Value: ", min_max_x)
        st.write("Min Max Y Value: ", min_max_y)
        st.write("Population Size: ", population_size)
        st.write("Number of Generations: ", ngen)
        st.write("Type of Problem: ", opt_type)
        if run_script_btn:
            logging.basicConfig(filename="saves/test.log", format='%(asctime)s %(message)s', filemode='w') 
            logger = logging.getLogger() 
            logger.setLevel(logging.DEBUG)
            # Execute script
            with st.spinner('Executing task...'):
                df = generate_dataframe(min_max_x, min_max_y, STEP)
                processed_output, df_results = genetic_algorithm(df, logger=logger, population_size=population_size, 
                                                                 num_bests=num_bests, CXPB=CXPB, MUTPB=MUTPB, minimize=minimize,
                                                                 ngen=ngen, id=st.session_state['id'])
                
                st.session_state['processed_output'] = processed_output
                st.session_state['df_results'] = df_results

            st.success('Optimization task completed!')
        if st.session_state['processed_output'] != []:
            st.session_state["output"] = True
    
    with tab3:
        if st.session_state["output"]:
            if not st.session_state['df_results'].empty:
                st.session_state['df_results'] = get_z_value(option=option, options=options, df=st.session_state['df_results'])
            
                fig = get_parallel_coodi(st.session_state['df_results'])
            
            # st.write('#### Species_id')
            # cols = st.columns(3)

            # category_list = df['species_id'].unique()
            # category = [None]*len(category_list)
            # for i,s in enumerate(category_list):
            #     with cols[i]:
            #         category[i] = st.checkbox(str(s), value=True)
            #         #st.write(category)

            # dff = df[df['species_id'].isin(category_list[category])].reset_index(drop=True)
            # fig = get_parallel_coodi(dff)
            
                final_df = pd.DataFrame([])
                tab_opt_graph, tab_df, tab_box = st.tabs(["Optimization Processing", "Best Individuals", "Box plot (Gen VS Individuals z-value)"])
                with tab_opt_graph:
                    st.plotly_chart(fig,use_container_width=True, theme="streamlit")
                with tab_df: 
                    st.write("Best 10 individuals in all generations: ")               
                    final_df["rank"] = np.arange(1,11,1)
                    final_df["individuals"] = st.session_state['processed_output'][:10]
                    final_df = get_z_value(option, options, final_df)
                    st.markdown(final_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)
                # st.write(st.session_state['processed_output'])
                with tab_box:
                    fig = get_box_plot(df=st.session_state['df_results'])
                    st.plotly_chart(fig,use_container_width=True, theme="streamlit")
        else:
            st.write("No output")
    
        
    if clear_btn:
        st.session_state["output"] = False
        st.session_state['disabled_btn'] = True
        st.session_state['id'] = ""
        st.session_state['df_results'] = pd.DataFrame([])
        st.session_state['processed_output'] = []
        st.rerun()
    
        
        
if __name__ == '__main__':
    main()