import streamlit as st

def show_about():
    st.markdown("---")
    st.header("👨‍💻 About the Author")
    st.image("https://rflyaqswtuuoukmvfhfc.supabase.co/storage/v1/object/public/product-mages/IMG_0638.jpg", width=150)

    st.markdown("""
                Hi there! I'm **Daniel Awuma**, the creator of this e-commerce app.  
                I'm a passionate **Python developer** who enjoys building user-friendly web apps, exploring data science, and experimenting with new tech stacks.

                I built this project using **Streamlit** to show how easy it can be to create a fully functional web app using pure Python — no heavy front-end frameworks required,
                Powered by a Supabase backend

                ### 🧠 My Interests
                - Web development with Python frameworks 
                - Python Backend Development  
                - Data Analytics

                ### 🔗 Connect with Me
                - 💼 [LinkedIn](https://www.linkedin.com/in/daniel-awuma-23201b22a/)  
                - 🐙 [GitHub](https://github.com/Pathogenic-cmd)  
                - ✉️ Email: awumadaniel015@gmail.com  

                Thanks for checking out my project! 🚀
                """
                )
