# Question 2.3: Researchly Dashboard Deployment

The Researchly dashboard classifies a pasted research abstract as
**artificial intelligence research** or **classical research**.

## Live Dashboard

[Open the Researchly dashboard](https://itnpa4-34researchly-npa-projectcristinaabrahamse-knnahyuwg7hfx.streamlit.app/)

The hosted dashboard can be accessed through a browser without
installing the project locally.

## Application Files

The application is located in the top-level
`Q1& Q2_Research_Papers` folder.

Keep these files together:

- `researchly_classifier_Q2.3.py` — Streamlit application.
- `best_research_abstract_classifier.joblib` — trained classification model.

The application locates the saved model relative to its own Python file.

## Run Locally

Download and extract the complete repository. Python must be installed.

Open a terminal in the extracted repository's root folder—the folder
containing `requirements.txt`.

### macOS

Run these commands one at a time:

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run "Q1& Q2_Research_Papers/researchly_classifier_Q2.3.py"
```

### Windows — PowerShell or Command Prompt

Run these commands one at a time:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run "Q1& Q2_Research_Papers/researchly_classifier_Q2.3.py"
```

If your Python installation uses `python` instead of `python3` or `py`,
substitute `python` in both commands.

Streamlit will display a local URL in the terminal. Open that address
in a browser if it does not open automatically.

## Dashboard Dependencies

The root `requirements.txt` specifies:

- Streamlit 1.51.0
- scikit-learn 1.7.2
- joblib 1.5.2

These dependencies support the dashboard application. Additional packages
are needed to run the analytical notebooks.

## Using Researchly

1. Paste a research abstract into the text box.
2. Select **Classify abstract**.
3. Review the predicted category and model score.

The prediction supports an initial review and should be checked against
the original research paper.
