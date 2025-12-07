import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")

def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Existing Examples ------------------------
def PolStratAdvHomeNav():
    st.sidebar.page_link("pages/00_Pol_Strat_Home.py", label="Political Strategist Home", icon="👤")

def WorldBankVizNav():
    st.sidebar.page_link("pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon="🏦")

def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")

def usaidWorkerHomeNav():
    st.sidebar.page_link("pages/10_USAID_Worker_Home.py", label="USAID Worker Home", icon="🏠")

def NgoDirectoryNav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")

def AddNgoNav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")

def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")

def PredictionNav():
    st.sidebar.page_link("pages/11_Prediction.py", label="Regression Prediction", icon="📈")

def ClassificationNav():
    st.sidebar.page_link("pages/13_Classification.py", label="Classification Demo", icon="🌺")



def TrainerLinks():
    st.sidebar.page_link("pages/1_trainer_homepage.py", label="Trainer Home", icon="🏋️")
    st.sidebar.page_link("pages/3_trainer_workout_templates.py", label="Workout Templates", icon="📝")
    st.sidebar.page_link("pages/4_trainer_client_programs.py", label="Client Programs", icon="🧑‍🤝‍🧑")
    st.sidebar.page_link("pages/5_trainer_client_logs.py", label="Client Logs", icon="📊")



def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link("pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢")



# Main Sidebar Handler Function
def SideBarLinks(show_home=False):

    # Display logo
    st.sidebar.image("assets/fitflow_logo.jpg", width=150)

    # Redirect unauthenticated users
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    # Show Home link
    if show_home:
        HomeNav()

    # Only show role-based links if logged in
    if st.session_state.get("authenticated"):

        role = st.session_state.get("role")

        if role == "pol_strat_advisor":
            PolStratAdvHomeNav()
            WorldBankVizNav()
            MapDemoNav()

        elif role == "usaid_worker":
            usaidWorkerHomeNav()
            NgoDirectoryNav()
            AddNgoNav()
            PredictionNav()
            ApiTestNav()
            ClassificationNav()

        elif role == "administrator":
            AdminPageNav()

        elif role == "trainer":
            TrainerLinks()

    # About always
    AboutPageNav()

    # Logout button
    if st.session_state.get("authenticated"):
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")