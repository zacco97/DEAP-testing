import streamlit as st

footnote = """
<style>a:link , a:visited{
color: #BFBFBF;  /* theme's text color hex code at 75 percent brightness*/
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: #0283C3; /* theme's primary color*/
background-color: transparent;
text-decoration: underline;
}

footer{
    visibility:hidden;
}

.link-container a {
  display:inline;
}

.footer {
  position: relative;
  left: 0px;
  top:0px;
  bottom: 0;
  width: 100%;
  background-color: transparent;
  color: #808080; /* theme's text color hex code at 50 percent brightness*/
  text-align: right; /* you can replace 'left' with 'center' or 'right' if you want*/
}
</style>


<div class="footer link-container">
  <p style='font-size: 0.875em;'> Made with <a href="https://streamlit.io/" target="_blank">Streamlit</a>
  by <a href="https://www.plusolutions.it/" target="_blank">PLUS</a>
  </p>
</div>

"""

sidebar = """<style>
    [data-testid="stSidebar"]{
        min-width: 0px;
        max-width: 600px;
    }
</style>
"""

hide_streamlit_style = """
          <style>
          #MainMenu {visibility: hidden;}
          footer {visibility: hidden;}
          header {visibility: hidden;}
          </style>
          """
