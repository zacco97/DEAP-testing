import streamlit as st
import numpy as np 
from styles import footnote, sidebar, hide_streamlit_style
from utils_app import get_plot, generate_dataframe, get_parallel_coodi
from genetic_alg import genetic_algorithm
import plotly.express as px
import json 
 
STEP = 0.15

f = open('app/options.json', "r")
options = json.loads(f.read())
    
def main():
    st.set_page_config(
        page_title="Genetic algorithms",
        page_icon=":bar_chart:",
        initial_sidebar_state="expanded"
        )
    
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
    option = st.selectbox('Which function do you want to optimize?', list(options.keys()))
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
        if run_script_btn:
            # Execute script
            with st.spinner('Executing task...'):
                df = generate_dataframe(min_max_x, min_max_y, STEP)
                processed_output = genetic_algorithm(df, logger=None, id=st.session_state['id'])
            st.success('Optimization task completed!')
            if processed_output is not None:
                st.session_state["output"] = True
        # st.write("Ideal GC content:", np.mean([gc_content[0], gc_content[1]]))
        # st.write("Number of the best pathogeans sequences to be downloaded:", num_bests)
        # st.write("Number of the best pathogeans sequences shown in graph:", 10)
    #     st.session_state.processed_output = []
    #     pass
    # if st.session_state.processed_output != []:
    
    with tab3:
        if st.session_state["output"]:
            df = px.data.iris()
            fig = get_parallel_coodi(df)

            st.write('#### Species_id')
            cols = st.columns(3)

            category_list = df['species_id'].unique()
            category = [None]*len(category_list)
            for i,s in enumerate(category_list):
                with cols[i]:
                    category[i] = st.checkbox(str(s), value=True)
                    #st.write(category)

            dff = df[df['species_id'].isin(category_list[category])].reset_index(drop=True)
            fig = get_parallel_coodi(dff)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        else:
            st.write("No output")
    
        
    if clear_btn:
        st.session_state["output"] = False
        st.session_state['disabled_btn'] = True
        st.session_state['id'] = ""
        st.rerun()
    
        
        
if __name__ == '__main__':
    main()