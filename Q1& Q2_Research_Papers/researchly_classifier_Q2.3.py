import html
import re
from pathlib import Path

import joblib
import streamlit as st


# Page setup 
st.set_page_config(
    page_title="Researchly | Abstract Classifier",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


MODEL_PATH = Path(__file__).parent / "best_research_abstract_classifier.joblib"


@st.cache_resource
def load_model():
    """Load the trained model once and reuse it while the app is running."""
    return joblib.load(MODEL_PATH)


def clean_abstract(text):
    """Apply the same text cleaning used before model prediction."""
    text = html.unescape(str(text))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = text.lower()
    text = re.sub(r"[^\w\s-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 8% 5%, #26365c 0, transparent 30%),
                linear-gradient(145deg, #101827 0%, #111827 55%, #171b32 100%);
            color: #f4f6fb;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2.2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, p, label {
            color: #f4f6fb;
        }

        .hero {
            padding: 1.7rem 2rem;
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 22px;
            background: linear-gradient(
                120deg,
                rgba(99, 102, 241, 0.22),
                rgba(34, 211, 238, 0.08)
            );
            margin-bottom: 1.5rem;
        }

        .eyebrow {
            color: #9fe8f3;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-size: 0.75rem;
            font-weight: 700;
        }

        .hero-title {
            font-size: clamp(2rem, 5vw, 3.2rem);
            line-height: 1.08;
            font-weight: 800;
            margin: 0.45rem 0 0.65rem 0;
        }

        .hero-copy {
            color: #cbd5e1;
            font-size: 1.05rem;
            max-width: 780px;
            margin-bottom: 0;
        }

        .stTextArea textarea {
            background: #182235 !important;
            color: #f8fafc !important;
            border: 1px solid #40506c !important;
            border-radius: 14px !important;
        }

        .stTextArea textarea:focus {
            border: 1px solid #67e8f9 !important;
            box-shadow: 0 0 0 2px rgba(103, 232, 249, 0.18) !important;
        }

        .stButton button,
        .stFormSubmitButton button {
            border: 0;
            border-radius: 12px;
            color: #08111f;
            background: linear-gradient(90deg, #67e8f9, #a5b4fc);
            font-weight: 750;
            min-height: 2.8rem;
            transition: 0.2s ease;
        }

        .stButton button:hover,
        .stFormSubmitButton button:hover {
            color: #08111f;
            border: 0;
            filter: brightness(1.08);
            transform: translateY(-1px);
        }

        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.055);
            border: 1px solid rgba(255, 255, 255, 0.10);
            padding: 1rem 1.1rem;
            border-radius: 16px;
        }

        .result-card {
            padding: 1.35rem 1.5rem;
            border-radius: 18px;
            border: 1px solid rgba(103, 232, 249, 0.38);
            background: linear-gradient(
                120deg,
                rgba(34, 211, 238, 0.13),
                rgba(99, 102, 241, 0.16)
            );
            margin-top: 1rem;
        }

        .result-label {
            color: #a5f3fc;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.72rem;
            font-weight: 700;
        }

        .result-value {
            color: #ffffff;
            font-size: 1.7rem;
            font-weight: 800;
            margin-top: 0.25rem;
        }

        .small-note {
            color: #aab6ca;
            font-size: 0.85rem;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# App heading
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Researchly · NLP project</div>
        <div class="hero-title">Give your abstract a first-pass review.</div>
        <p class="hero-copy">
            Paste a research abstract and the machine-learning model will
            classify it as artificial-intelligence research or classical research.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# Performance figures from the held-out test set
metric_1, metric_2, metric_3 = st.columns(3)

with metric_1:
    st.metric("Held-out test accuracy", "93.8%")

with metric_2:
    st.metric("Macro F1-score", "89.6%")

with metric_3:
    st.metric("Model selected", "Tuned Extra Trees")


left_column, right_column = st.columns([1.8, 1], gap="large")


with left_column:
    st.subheader("Try an abstract")
    st.caption("The abstract text is used for this prediction.")

    with st.form("abstract_classifier_form"):
        abstract = st.text_area(
            "Research abstract",
            height=250,
            placeholder=(
                "Paste the abstract here…\n\n"
                "For example, include the study's purpose, methods and findings."
            ),
            label_visibility="collapsed",
        )

        classify_clicked = st.form_submit_button(
            "Classify abstract",
            use_container_width=True,
        )

    if classify_clicked:
        cleaned_abstract = clean_abstract(abstract)

        if not cleaned_abstract:
            st.warning("Add an abstract first, then click the classify button.")
        else:
            with st.spinner("Reading the abstract…"):
                try:
                    model = load_model()
                    prediction = model.predict([cleaned_abstract])[0]

                    class_names = {
                        "ai": "Artificial intelligence research",
                        "classical": "Classical research",
                    }
                    result = class_names.get(
                        str(prediction).lower(),
                        str(prediction).replace("_", " ").title(),
                    )

                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="result-label">Researchly prediction</div>
                            <div class="result-value">{html.escape(result)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Show the model's score if the saved classifier 
                    if hasattr(model, "predict_proba"):
                        probabilities = model.predict_proba([cleaned_abstract])[0]
                        classes = list(model.classes_)
                        predicted_index = classes.index(prediction)
                        score = float(probabilities[predicted_index])

                        st.write(f"Model score: **{score:.1%}**")
                        st.progress(score)
                        st.caption(
                            "This score reflects the model's estimate; it is "
                            "not a guarantee that the classification is correct."
                        )

                except FileNotFoundError:
                    st.error(
                        "I couldn't find the saved model. Make sure "
                        "`best_research_abstract_classifier.joblib` is in the "
                        "same folder as this Python file."
                    )


with right_column:
    st.subheader("How to use it")

    st.markdown(
        """
        **1.** Paste a research abstract.  
        **2.** Select **Classify abstract**.  
        **3.** Review the predicted research category.
        """
    )

    st.info(
        "This is a screening aid for a first-pass review. "
        "Check the original paper before making a final decision."
    )

    st.markdown("#### About this prototype")
    st.markdown(
        """
        - Text is cleaned before it is sent to the trained model.
        - The tuned Extra Trees model was selected during model comparison.
        - Test results shown above come from the held-out evaluation set.
        """
    )


st.markdown(
    """
    <p class="small-note" style="text-align:center; margin-top:3rem;">
        A student-built NLP prototype · Designed by Cristina Abrahamse· 2026
    </p>
    """,
    unsafe_allow_html=True,
)