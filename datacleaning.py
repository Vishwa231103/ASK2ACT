import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ASK2ACT",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- PERFECT DARK THEME (NO WHITE STRIPS) ----------------
st.markdown("""
<style>

/* Remove default Streamlit padding */
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* Remove header + footer white areas */
header, footer {
    visibility: hidden;
}

/* Main background full dark */
.stApp {
    background: linear-gradient(180deg, #0b1220 0%, #0a0f1c 100%);
}

/* Remove top white bar */
div[data-testid="stToolbar"] {
    visibility: hidden;
}

/* Text colors */
h1, h2, h3, h4, h5, h6, p, label, span {
    color: #ffffff !important;
}

/* Remove horizontal line */
hr {
    border: none !important;
}

/* Upload section styling */
[data-testid="stFileUploader"] {
    background-color: #1f2937 !important;
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #2d3748;
}

/* Remove inner white drop area */
[data-testid="stFileUploaderDropzone"] {
    background-color: #111827 !important;
    border: 2px dashed #374151 !important;
    color: #ffffff !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #ffffff !important;
}

[data-testid="stFileUploaderDropzone"] div {
    background: transparent !important;
}

/* Fix Browse Files button */
[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploader"] button:hover {
    opacity: 0.9 !important;
}

[data-testid="stFileUploader"] * {
    color: #ffffff !important;
}

/* Info box styling */
div[data-testid="stAlert"] {
    background-color: #13203a !important;
    color: white !important;
    border-radius: 12px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white !important;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    border: none;
}

.stButton>button:hover {
    opacity: 0.9;
}

/* Fix Download Button */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
}

[data-testid="stDownloadButton"] button:hover {
    opacity: 0.9 !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- CENTERED HEADER ----------------
st.markdown("""
<div style='text-align:center; padding:30px 0;'>
    <h1 style='font-size:48px;'>🤖 ASK2ACT</h1>
    <p style='color:#9ca3af; font-size:18px;'>AI-powered Data Cleaning Tool</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FILE UPLOAD ----------------
file = st.file_uploader("Upload CSV file", type=["csv"])

# ---------------- MAIN LOGIC ----------------
if file:
    df = pd.read_csv(file)

    st.subheader("Cleaning Options")

    col1, col2 = st.columns(2)

    with col1:
        remove_duplicates = st.checkbox("Remove duplicate rows")
        drop_missing_rows = st.checkbox("Drop rows with missing values")
        fill_missing = st.checkbox("Forward fill missing values")
        standardize_cols = st.checkbox("Standardize column names")

    with col2:
        lowercase_text = st.checkbox("Convert text to lowercase")
        strip_whitespace = st.checkbox("Remove extra whitespace")
        remove_columns = st.multiselect("Drop selected columns", df.columns)

    if st.button("🚀 Process Data"):
        cleaned_df = df.copy()

        if remove_duplicates:
            cleaned_df = cleaned_df.drop_duplicates()

        if drop_missing_rows:
            cleaned_df = cleaned_df.dropna()

        if fill_missing:
            cleaned_df = cleaned_df.fillna(method="ffill")

        if standardize_cols:
            cleaned_df.columns = (
                cleaned_df.columns.str.lower()
                .str.strip()
                .str.replace(" ", "_")
            )

        if lowercase_text:
            for col in cleaned_df.select_dtypes(include="object"):
                cleaned_df[col] = cleaned_df[col].str.lower()

        if strip_whitespace:
            for col in cleaned_df.select_dtypes(include="object"):
                cleaned_df[col] = cleaned_df[col].str.strip()

        if remove_columns:
            cleaned_df = cleaned_df.drop(columns=remove_columns)

        st.markdown("---")
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Original Data")
            st.dataframe(df, use_container_width=True)

        with c2:
            st.subheader("Cleaned Data")
            st.dataframe(cleaned_df, use_container_width=True)

        csv = cleaned_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Cleaned CSV", csv, "cleaned_data.csv")

else:
    st.info("👆 Upload a CSV file to get started")
