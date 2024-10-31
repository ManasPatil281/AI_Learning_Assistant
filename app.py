import streamlit as st
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import random
import json
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv



load_dotenv()



YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
# Title for the application
st.title("👩‍🎓 AI Learning Assistant👨‍🎓")


st.sidebar.title("👩‍🔧 Select your Preferences🧑‍⚕️")

subjects_data = {
    "CBSE": {
        "11": ["Mathematics", "Physics", "Chemistry", "Biology"],
        "12": ["Mathematics", "Physics", "Chemistry", "Biology"],
    },
    "ICSE": {
        "11": ["Mathematics", "Physics", "Chemistry", "Biology"],
        "12": ["Mathematics", "Physics", "Chemistry", "Biology"],
    },

     "Maharashtra": {
            "11": ["Mathematics", "Physics", "Chemistry", "Biology"],
            "12": ["Mathematics", "Physics", "Chemistry", "Biology"],
        }

}

# Content data for each subject
content_data = {
    "CBSE": {
        "11": {
            "Mathematics": [
                "1. Sets",
                "2. Relations and Functions",
                "3. Trigonometric Functions",
                "4. Principle of Mathematical Induction",
                "5. Complex Numbers and Quadratic Equations",
                "6. Linear Inequalities",
                "7. Permutations and Combinations",
                "8. Binomial Theorem",
                "9. Sequences and Series",
                "10. Straight Lines",
                "11. Conic Sections",
                "12. Introduction to Three-dimensional Geometry",
                "13. Limits and Derivatives",
                "14. Mathematical Reasoning",
                "15. Statistics",
                "16. Probability"
            ],
            "Physics": [
                "1. Physical World",
                "2. Units and Measurements",
                "3. Motion in a Straight Line",
                "4. Motion in a Plane",
                "5. Laws of Motion",
                "6. Work, Energy and Power",
                "7. System of Particles and Rotational Motion",
                "8. Gravitation",
                "9. Mechanical Properties of Solids",
                "10. Mechanical Properties of Fluids",
                "11. Thermal Properties of Matter",
                "12. Thermodynamics",
                "13. Kinetic Theory",
                "14. Oscillations",
                "15. Waves"
            ],
            "Chemistry": [
                "1. Some Basic Concepts of Chemistry",
                "2. Structure of Atom",
                "3. Classification of Elements and Periodicity in Properties",
                "4. Chemical Bonding and Molecular Structure",
                "5. States of Matter: Gases and Liquids",
                "6. Thermodynamics",
                "7. Equilibrium",
                "8. Redox Reactions",
                "9. Hydrogen",
                "10. The s-Block Element",
                "11. The p-Block Element",
                "12. Organic Chemistry - Some Basic Principles and Techniques",
                "13. Hydrocarbons",
                "14. Environmental Chemistry"
            ],
            "Biology": [
                "1. The Living World",
                "2. Biological Classification",
                "3. Plant Kingdom",
                "4. Animal Kingdom",
                "5. Morphology of Flowering Plants",
                "6. Anatomy of Flowering Plants",
                "7. Structural Organisation in Animals",
                "8. Cell: The Unit of Life",
                "9. Biomolecules",
                "10. Cell Cycle and Cell Division",
                "11. Transport in Plants",
                "12. Mineral Nutrition",
                "13. Photosynthesis in Higher Plants",
                "14. Respiration in Plants",
                "15. Plant - Growth and Development",
                "16. Digestion and Absorption",
                "17. Breathing and Exchange of Gases",
                "18. Body Fluids and Circulation",
                "19. Excretory Products and their Elimination",
                "20. Locomotion and Movement",
                "21. Neural Control and Coordination",
                "22. Chemical Coordination and Integration"
            ]
        },
        "12": {
            "Mathematics": [
                "1. Relations and Functions",
                "2. Inverse Trigonometric Functions",
                "3. Matrices",
                "4. Determinants",
                "5. Continuity and Differentiability",
                "6. Applications of Derivatives",
                "7. Integrals",
                "8. Applications of Integrals",
                "9. Differential Equations",
                "10. Vector Algebra",
                "11. Three-dimensional Geometry",
                "12. Linear Programming",
                "13. Probability"
            ],
            "Physics": [
                "1. Electric Charges and Fields",
                "2. Electrostatic Potential and Capacitance",
                "3. Current Electricity",
                "4. Moving Charges and Magnetism",
                "5. Magnetism and Matter",
                "6. Electromagnetic Induction",
                "7. Alternating Currents",
                "8. Electromagnetic Waves",
                "9. Optics",
                "10. Wave Optics",
                "11. Dual Nature of Radiation and Matter",
                "12. Atoms",
                "13. Nuclei",
                "14. Semiconductor Electronics",
                "15. Communication Systems"
            ],
            "Chemistry": [
                "1. The Solid State",
                "2. Solutions",
                "3. Electrochemistry",
                "4. Chemical Kinetics",
                "5. Surface Chemistry",
                "6. General Principles and Processes of Isolation of Elements",
                "7. p-Block Elements",
                "8. d and f Block Elements",
                "9. Coordination Compounds",
                "10. Haloalkanes and Haloarenes",
                "11. Alcohols, Phenols and Ethers",
                "12. Aldehydes, Ketones and Carboxylic Acids",
                "13. Organic Compounds Containing Nitrogen",
                "14. Biomolecules",
                "15. Polymers",
                "16. Chemistry in Everyday Life"
            ],
            "Biology": [
                "1. Reproduction in Organisms",
                "2. Sexual Reproduction in Flowering Plants",
                "3. Human Reproduction",
                "4. Reproductive Health",
                "5. Principles of Inheritance and Variation",
                "6. Molecular Basis of Inheritance",
                "7. Evolution",
                "8. Human Health and Disease",
                "9. Strategies for Enhancement in Food Production",
                "10. Microbes in Human Welfare",
                "11. Biotechnology - Principles and Processes",
                "12. Biotechnology and its Applications",
                "13. Organisms and Populations",
                "14. Ecosystem",
                "15. Biodiversity and Conservation",
                "16. Environmental Issues"
            ]
        }
    },
    "ICSE": {
        "11": {
            "Mathematics": [
                "1.Sets and Functions",
"2.Complex Numbers",
"3.Quadratic Equations",
"4.Permutations and Combinations",
"5.Binomial Theorem",
"6.Sequences and Series",
"7.Straight Lines",
"8.Conic Sections",
"9.Introduction to Three-Dimensional Geometry",
"10.Limits and Derivatives",
"11.Mathematical Reasoning",
"12.Statistics",
"13.Probability"
            ],
            "Physics": [
                "1.Measurement",
"2.Kinematics",
"3.Dynamics",
"4.Work, Energy, and Power",
"5.Motion of System of Particles and Rigid Body",
"6.Gravitation",
"7.Properties of Matter",
"8.Heat",
"9.Wave Motion",
"10.Sound",
"11.Light",
"12.Electricity",
"13.Magnetism",
"14.Modern Physics",
            ],
            "Chemistry": [
                "1. Basic Concepts of Chemistry",
                "2. Structure of Atom",
                "3. Periodic Table and Periodicity",
                "4. Chemical Bonding and Molecular Structure",
                "5. States of Matter",
                "6. Thermodynamics",
                "7. Equilibrium",
                "8. Redox Reactions",
                "9. Hydrogen",
                "10. s-Block and p-Block Elements",
                "11. Organic Chemistry - Basic Principles",
                "12. Hydrocarbons",
                "13. Environmental Chemistry"
            ],
            "Biology": [
                "1.Cell: Structure and Function",
"2.Biomolecules",
"3.Cell Division",
"4.Plant Kingdom",
"5.Animal Kingdom",
"6.Structural Organisation in Animals and Plants",
"7.Human Physiology",
"8.Ecology and Environment"
            ]
        },
        "12": {
            "Mathematics": [
                "1.Relations and Functions",
"2.Algebra"
"3.Calculus"
"4.Vectors"
"5.Three-Dimensional Geometry"
"6.Statistics"
"7.Probability"
"8.Linear Programming"
"9.Mathematical Reasoning"
            ],
            "Physics": [
                "1. Electrostatics",
                "2. Current Electricity",
                "3. Magnetism",
                "4. Electromagnetic Induction",
                "5. Alternating Currents",
                "6. Electromagnetic Waves",
                "7. Optics",
                "8. Dual Nature of Radiation",
                "9. Atoms and Nuclei",
                "10. Electronic Devices",

            ],
            "Chemistry": [
                "1. Solutions",
                "2. Electrochemistry",
                "3. Chemical Kinetics",
                "4. Surface Chemistry",
                "5. General Principles of Isolation of Elements",
                "6. p-Block Elements",
                "7. d-Block and f-Block Elements",
                "8. Coordination Compounds",
                "9. Haloalkanes and Haloarenes",
                "10. Alcohols, Phenols, and Ethers",
                "11. Carbonyl Compounds",
                "12.Carboxylic Acids",
                "13. Organic Compounds Containing Nitrogen",
                "14. Biomolecules",
                "15. Polymers",
                "16. Chemistry in Everyday Life"
            ],
            "Biology": [
                "1. Reproduction",
                "2. Genetics and Evolution",
                "3. Biotechnology and its Applications",
                "4. Ecology and Environment",
            ]
        }
    },
    "Maharashtra": {
        "11": {
            "Mathematics": [
                "1.Angle and Its Measurement",
    "2.Trigonometry - 1",
    "3.Trigonometry - 2",
    "4.Determinants and Matrices",
    "5.Straight Line",
    "6.Circle",
    "7.Conic Sections",
    "8.Measures of Dispersion",
    "9.Probability",
    "10.Complex Numbers",
    "11.Sequences and Series",
    "12.Permutations and Combination",
    "13.Methods of Induction and Binomial Theorem",
    "14.Sets and Relations",
    "15.Functions",
    "16.Limits",
    "17.Continuity",
    "18.Differentiation"
            ],
            "Physics": [
                "1.Units and Measurements",
                "2.Mathematical Methods",
                "3.Motion in a Plane",
                "4.Laws of Motion",
                "5.Gravitation",
                "6.Mechanical Properties of Solids",
                "7.Thermal Properties of Matter",
                "8.Sound",
                "9.Optics",
                "10.Electrostatics",
                "11.Electric Current Through Conductors",
                "12.Magnetism",
                "13.Electromagnetic Waves and Communication System",
                "14.Semiconductors"
            ],
            "Chemistry": [
                "1.Some Basic Concepts of Chemistry",
                "2.Structure of Atom",
                "3.Classification of Elements and Periodicity in Properties",
                "4.Chemical Bonding and Molecular Structure",
                "5.States of Matter: Gases and Liquids",
                "6.Thermodynamics",
                "7.Equilibrium",
                "8.Redox Reactions",
                "9.Hydrogen",
                "10.s-Block Element (Alkali and Alkaline earth metals)",
                "11.Some p-Block Elements",
                "12.Organic Chemistry - Some Basic Principles and Techniques",
                "13.Hydrocarbons",
                "14.Environmental Chemistry"
            ],
            "Biology": [
                 "1.Living World",
                 "2.Systematics of Living Organisms",
    "3.Kingdom Plantae",
    "4.Kingdom Animalia",
    "5.Cell Structure and Organization",
    "6.Biomolecules",
    "7.Cell Division",
    "8.Plant Tissues and Anatomy",
    "9.Morphology of Flowering Plants",
    "10.Animal Tissue",
    "11.Study of Animal Type: Cockroach",
    "12.Photosynthesis",
    "13.Respiration and Energy Transfer",
    "14.Human Nutrition",
    "15.Excretion and Osmoregulation",
    "16.Skeleton and Movement"
            ]
        },
        "12": {
            "Mathematics": [
                "1.Relations and Functions",
                "2.Inverse Trigonometric Functions",
                "3.Matrices",
                "4.Determinants",
                "5.Continuity and Differentiability",
                "6.Applications of Derivatives",
                "7.Integrals",
                "8.Applications of Integrals",
                "9.Differential Equations",
                "10.Vector Algebra",
                "11.Three-dimensional Geometry",
                "12.Linear Programming",
                "13.Probability"
            ],
            "Physics": [
                "1.Electric Charges and Fields",
"2.Electrostatic Potential and Capacitance",
"3.Current Electricity",
"4.Moving Charges and Magnetism",
"5.Magnetism and Matter",
"6.Electromagnetic Induction",
"7.Alternating Currents",
"8.Electromagnetic Waves",
"9.Ray Optics and Optical Instruments",
"10.Wave Optics",
"11.Dual Nature of Radiation and Matter",
"12.Atoms and Nuclei",
"13.Electronic Devices"],

            "Chemistry": [
                "1.Solid State",
"2.Solutions",
"3.Electrochemistry",
"4.Chemical Kinetics",
"5.Surface Chemistry",
"6.General Principles and Processes of Isolation of Elements",
"7.p-Block Elements",
"8.d and f Block Elements",
"9.Coordination Compounds",
"10.Haloalkanes and Haloarenes",
"11.Alcohols, Phenols, and Ethers",
"12.Carbonyl Compounds",
"13.Carboxylic Acids and Their Derivatives",
"14.Biomolecules",
"15.Polymers",
"16.Chemistry in Everyday Life",
            ],
            "Biology": [
                "1.Reproduction in Organisms",
"2.Sexual Reproduction in Flowering Plants",
"3.Human Reproduction",
"4.Principles of Inheritance and Variation",
"5.Molecular Basis of Inheritance",
"6.Evolution",
"7.Biotechnology Principles",
"8.Biotechnology and its Applications in Medicine",
"9.Ecosystem",
"10.Biodiversity and Conservation",
"11.Environmental Issues",
            ]
        }
    }
}



board = st.sidebar.selectbox("Select Board", ["Maharashtra", "ICSE", "CBSE"])

# If "State" board is selected, show an additional dropdown for selecting the state


standard = st.sidebar.selectbox("Select Standard", ["11", "12"])

subject = st.sidebar.selectbox("Select Subject", subjects_data[board][standard])

chapter=st.sidebar.selectbox(("Select Chapter"),content_data[board][standard][subject])




# Form for creating short notes
with st.form("Short Notes"):
    s_notes = st.form_submit_button("📋 Create Short Notes 📋")

    if s_notes:

        def generate_short_notes(board, standard, subject, chapter):
            prompt = (f"Create concise ,brief ,including a section which student tend to  neglect  and informative short notes for {subject}, "
                      f"Chapter: {chapter} as per {board} {standard} curriculum.")

            try:
                response = model.generate_content(
                    prompt
                )
                return response.text

            except Exception as e:
                return "Error generating short notes: " + str(e)


        # Generate and display the notes
        notes = generate_short_notes(board, standard, subject, chapter)
        st.write("### Short Notes")
        st.write(notes)

with st.form("Formulas"):
    formula = st.form_submit_button("⚛️ Get Formulas ⚛️")

    if formula:

        def formulas(board, standard, subject, chapter):
            prompt = (f"Create a formula list  for {subject}, "
                      f"Chapter: {chapter} as per {board} {standard} curriculum.")

            try:
                response = model.generate_content(
                    prompt
                )
                return response.text

            except Exception as e:
                return "Error generating short notes: " + str(e)


        # Generate and display the notes
        notes = formulas(board, standard, subject, chapter)
        st.write("### Formula list")
        st.write(notes)

with st.form("questions"):
    questions= st.form_submit_button("📑📊Get questions📊📑")

    if questions:

        def get_questions(board, standard, subject, chapter):
            prompt = (f"Create atleast 10 most important questions (thoerotical as well as numericals)  which are frequently asked for {subject}, "
                      f"Chapter: {chapter} as per {board} {standard} curriculum.")

            try:
                response = model.generate_content(
                    prompt
                )
                return response.text

            except Exception as e:
                return "Error generating short notes: " + str(e)


        # Generate and display the notes
        notes = get_questions(board, standard, subject, chapter)
        st.write("### questions")
        st.write(notes)


with st.form("PYQS"):
    pyqs= st.form_submit_button("📇 Get PYQS 📇")

    if pyqs:

        def get_pyqs(board, standard, subject, chapter):
            prompt = (f"Give the most trending, hot and important mcq pyqs from jee mains,neet and advance atleast 15 for {subject}, "
                      f"Chapter: {chapter} as per {board} {standard} curriculum.")

            try:
                response = model.generate_content(
                    prompt
                )
                return response.text

            except Exception as e:
                return "Error generating short notes: " + str(e)


        # Generate and display the notes
        notes = get_pyqs(board, standard, subject, chapter)
        st.write("### pyqs")
        st.write(notes)









# Streamlit form for user input
with st.form("YouTube Videos"):

    videos = st.form_submit_button("▶️🎦Get Youtube videos links 🎦▶️")

    if videos:

        def get_youtube_videos(subject, chapter, board):
            search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={subject}{chapter}{board}+tutorial&type=video&key={YOUTUBE_API_KEY}"

            try:
                response = requests.get(search_url)
                data = response.json()
                video_list = []

                for item in data.get('items', []):
                    video_title = item['snippet']['title']
                    video_id = item['id'].get('videoId')
                    if video_id:  # Check if videoId exists
                        video_url = f"https://www.youtube.com/watch?v={video_id}"
                        video_list.append((video_title, video_url))

                return video_list

            except Exception as e:
                return [f"Error fetching YouTube videos: {str(e)}"]


        # Generate and display the video links
        links = get_youtube_videos(subject, chapter, board)
        st.write("*YouTube Videos:*")

        if links:
            for title, url in links:
                st.write(f"- [{title}]({url})")
        else:
            st.write("No videos found.")



with st.form("Books Recommendations"):
    books= st.form_submit_button("📚 Get Books Recommendations 📚")

    if books:

        def get_books(board, standard, subject, chapter):
            prompt = (f"Give the book recommendation  for {subject}, "
                      f"Chapter: {chapter} as per {board} {standard} curriculum.")

            try:
                response = model.generate_content(
                    prompt
                )
                return response.text

            except Exception as e:
                return "Error generating short notes: " + str(e)


        # Generate and display the notes
        book = get_books(board, standard, subject, chapter)
        st.write("### Books")
        st.write(book)


def ask_query(chat):
    prompt = f"Solve the query as if you are his teacher: {chat}"

    try:
        # Generate response using the model
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return "Error generating response: " + str(e)


chat = st.text_input("❓❓Ask any query❓❓")

if chat:
    solution = ask_query(chat)
    st.write(solution)


st.markdown('''
<style>
    /* General background with gradient */
    .reportview-container {
        background: linear-gradient(135deg, #2196f3, #e3f2fd);
        padding: 20px;
        font-family: 'Roboto', sans-serif;
    }

    /* Header styling with shadow and gradient text */
    h1, .title {
        color: #1a237e;
        font-size: 3.5em;
        font-weight: 800;
        background: linear-gradient(to right, #42a5f5, #1e88e5);
        -webkit-background-clip: text;
        color: black;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px #e3f2fd;
    }

    /* Sidebar and panel styles */
    .sidebar .sidebar-content {
        background-color: #e3f2fd;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        font-size: 2.1em;
        color: #0d47a1;
    }

    /* Enhanced button styling */
    .stButton>button {
        background: linear-gradient(135deg, #42a5f5, #1e88e5);
        color: white;
        font-size: 2.1em;
        font-weight: 600;
        padding: 12px 25px;
        border: none;
        border-radius: 8px;
        box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1e88e5, #42a5f5);
        transform: translateY(-2px);
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
    }

    /* Container styling with rounded borders and shadow */
    .container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
        font-size: 2.1em;
    }

    /* Animations */
    .fade-in {
        animation: fadeIn 0.8s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

</style>
''', unsafe_allow_html=True)