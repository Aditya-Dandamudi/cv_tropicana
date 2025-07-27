# import streamlit as st
# from PIL import Image
# from lib import *
# from base64 import b64encode

# # --------- PAGE CONFIG --------- #
# st.set_page_config(page_title="🥤Tropicana Classifier", layout="centered")

# # --------- ENCODE LOGO --------- #
# def get_base64_logo(path):
#     with open(path, "rb") as img_file:
#         return b64encode(img_file.read()).decode()

# logo_base64 = get_base64_logo("Tropicana-Logo.png")

# # --------- CUSTOM CSS --------- #
# st.markdown(f"""
#     <style>
#         html, body {{
#             background-color: #e6f9e6;
#             height: 100%;
#             margin: 0;
#             padding: 0;
#         }}
#         .block-container {{
#             padding-top: 0rem;
#             background-color: #e6f9e6;
#         }}
#         .logo-container {{
#             display: flex;
#             justify-content: center;
#             padding: 2rem 0 1rem 0;
#         }}
#         .logo {{
#             height: 140px;
#             transition: transform 0.3s ease-in-out;
#         }}
#         .logo.animate {{
#             animation: pulse 1.5s infinite;
#         }}
#         @keyframes pulse {{
#             0% {{ transform: scale(1); }}
#             50% {{ transform: scale(1.1); }}
#             100% {{ transform: scale(1); }}
#         }}
#         .top-bar {{
#             background-color: #f95c14;
#             padding: 1rem 2rem;
#             color: white;
#             font-size: 30px;
#             font-weight: bold;
#             text-align: center;
#             border-bottom: 3px solid #ff7c33;
#             box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
#             margin-bottom: 2rem;
#         }}
#         [data-testid="stFileUploader"] > div:first-child {{
#             background-color: #fff0e5;
#             border: 2px dashed #f95c14;
#             border-radius: 10px;
#             padding: 1rem;
#             color: #333;
#         }}
#     </style>

#     <div class="logo-container">
#         <img class="logo" id="main-logo" src="data:image/png;base64,{logo_base64}" alt="Tropicana Logo">
#     </div>
#     <div class="top-bar">
#         Tropicana Product Classifier 🥤
#     </div>

#     <script>
#         const logo = window.parent.document.getElementById("main-logo");
#         const observer = new MutationObserver(mutations => {{
#             for (let mutation of mutations) {{
#                 if (mutation.target.innerText.includes("Classifying...")) {{
#                     logo.classList.add("animate");
#                 }} else {{
#                     logo.classList.remove("animate");
#                 }}
#             }}
#         }});
#         const target = window.parent.document.querySelector('.element-container');
#         if (target) {{
#             observer.observe(target, {{ childList: true, subtree: true }});
#         }}
#     </script>
# """, unsafe_allow_html=True)

# # --------- LOAD MODEL --------- #
# @st.cache_resource
# def get_model():
#     return load_model("best.pt")

# model = get_model()

# # --------- UI --------- #
# st.markdown("Upload an image of a Tropicana product, and our AI model will classify it for you.")

# conf = st.slider("Your Preferred Confidence Threshold", min_value=0.0, max_value=1.0, value=0.25, step=0.01)

# uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# # --------- PREDICTION --------- #
# if uploaded_file:
#     st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

#     with st.spinner("🔍 Classifying..."):
#         img = Image.open(uploaded_file)
#         prediction = predict_top_label(model, img, conf_threshold=conf)

#     st.markdown("---")
#     if prediction:
#         st.success("✅ Prediction Result:")
#         st.markdown(f"<div style='font-size: 20px; color:#333;'>{prediction}</div>", unsafe_allow_html=True)
#     else:
#         st.warning("⚠️ No products confidently identified at the selected threshold.")




import streamlit as st
from PIL import Image
from lib import load_model, predict_image
from base64 import b64encode

# --- PAGE CONFIG ---
st.set_page_config(page_title="🥤Tropicana Classifier", layout="centered")

# --- ENCODE LOGO ---
def get_base64_logo(path):
    with open(path, "rb") as img_file:
        return b64encode(img_file.read()).decode()

logo_base64 = get_base64_logo("Tropicana-Logo.png")

# --- CUSTOM CSS + LOGO + BAR ---
st.markdown(f"""
    <style>
        html, body {{
            background-color: #e6f9e6;
            height: 100%;
            margin: 0;
            padding: 0;
        }}
        .block-container {{
            padding-top: 0rem;
            background-color: #e6f9e6;
        }}
        .logo-container {{
            display: flex;
            justify-content: center;
            padding: 2rem 0 1rem 0;
        }}
        .logo {{
            height: 140px;
            transition: transform 0.3s ease-in-out;
        }}
        .logo.animate {{
            animation: pulse 1.5s infinite;
        }}
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); }}
        }}
        .top-bar {{
            background-color: #f95c14;
            padding: 1rem 2rem;
            color: white;
            font-size: 30px;
            font-weight: bold;
            text-align: center;
            border-bottom: 3px solid #ff7c33;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}
        [data-testid="stFileUploader"] > div:first-child {{
            background-color: #fff0e5;
            border: 2px dashed #f95c14;
            border-radius: 10px;
            padding: 1rem;
            color: #333;
        }}
    </style>

    <div class="logo-container">
        <img class="logo" id="main-logo" src="data:image/png;base64,{logo_base64}" alt="Tropicana Logo">
    </div>
    <div class="top-bar">
        Tropicana Product Classifier 🥤
    </div>

    <script>
        const logo = window.parent.document.getElementById("main-logo");
        const observer = new MutationObserver(mutations => {{
            for (let mutation of mutations) {{
                if (mutation.target.innerText.includes("Detecting")) {{
                    logo.classList.add("animate");
                }} else {{
                    logo.classList.remove("animate");
                }}
            }}
        }});
        const target = window.parent.document.querySelector('.element-container');
        if (target) {{
            observer.observe(target, {{ childList: true, subtree: true }});
        }}
    </script>
""", unsafe_allow_html=True)

# --- LOAD MODEL ---
@st.cache_resource
def get_model():
    return load_model("best.pt")

model = get_model()

# --- UI INSTRUCTIONS ---
st.markdown("Upload an image of a Tropicana product, and our AI model will detect and classify it.")
conf = st.slider("Confidence Threshold", min_value=0.0, max_value=1.0, value=0.25, step=0.01)

# --- FILE UPLOAD ---
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# --- PREDICTION WORKFLOW ---
if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    with st.spinner("🔍 Detecting..."):
        img = Image.open(uploaded_image)
        result_image = predict_image(model, img, conf_threshold=conf)
    st.image(result_image, caption="Detected Image", use_column_width=True)