import streamlit as st
import numpy as np 
from styles import footnote, sidebar, hide_streamlit_style
from utils_app import get_plot


STEP = 0.15
options = {'Rosenbrock function':"id1", 
           'sin(x) + cos(y)':"id2", 
           '(x² + y — 11)² + (x + y² — 7)²':"id3"}
    
def main():
    st.set_page_config(
        page_title="Genetic algorithms",
        page_icon=":bar_chart:",
        initial_sidebar_state="expanded"
        )
    
    # st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.write(footnote, unsafe_allow_html=True)
    st.title('Testing GA for optimization')
    
    np.random.seed(100)
    st.markdown(sidebar, unsafe_allow_html=True)
    st.sidebar.title("Parameters")
    
    min_max_x = st.sidebar.slider("Min Max X Value:", -5.0, 5.0, (-2.0, 2.0), step=STEP)
    min_max_y = st.sidebar.slider("Min Max Y Value:", -5.0, 5.0, (-2.0, 2.0), step=STEP)
    option = st.selectbox('Which function do you eant to optimize?', list(options.keys()))

    # submit = st.button('Generate Graph')
    tab1, tab2, tab3 = st.tabs(["Graph", "Parameters", "Results"])
   
    with tab1:
        submit = st.button('Generate Graph')
        if submit:
            st.write("3D Plot of the function: ", option)
            fig = get_plot(option, options, min_max_x, min_max_y, STEP)
            st.plotly_chart(fig)
        
            col1, col2 = st.sidebar.columns([1,1])
            clear = col2.button('Clear')
            run_script = col1.button("Run Script", type="primary")
    
    with tab2:
        st.session_state.processed_output = []
        pass
    if st.session_state.processed_output != []:
        with tab3:
            pass
        
        # if clear:
        #     # st.session_state["value"] = 0
        #     # st.session_state["conditions"] = []
        #     st.experimental_rerun()
        
        # if run_script:
        #     # Execute script
        #     with st.spinner('Executing task...'):
        #         processed_output = process_script(new_df=df, proximity_limit=proximity_limit, 
        #                                         gc_content_max=gc_content[1], gc_content_min=gc_content[0],
        #                                         population_size=population_size, num_bests=num_bests, 
        #                                         CXPB=CXPB, MUTPB=MUTPB, num_generations=num_generations,
        #                                         conditions=conditions)
        #         st.session_state.show_info = True
        #     st.session_state.processed_output = read_results(processed_output)
        
        # if st.session_state.processed_output != []:        
        #     # Display completion message
        #     processed_output = st.session_state.processed_output
        
        
if __name__ == '__main__':
    
    
    main()