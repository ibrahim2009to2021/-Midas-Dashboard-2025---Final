import streamlit as st

def render_chatbot():
    """
    Renders the Tawk.to chatbot widget by injecting its JavaScript code.
    """
    <!--Start of Tawk.to Script-->
<script type="text/javascript">
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/68f6aa005eca4d194faaeca2/1j81og4l1';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();
</script>
<!--End of Tawk.to Script-->
   
    """
    
    # Use Streamlit's HTML component to inject the script into the app
    st.components.v1.html(tawk_to_code, height=0)


