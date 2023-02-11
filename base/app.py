# Shaheer Syed
# This work was inspired by the ESM Fold Protein Structure Prediction by Meta
# Note: With Streamlit -- Python Script is read from top-to-bottom;
# Therefore, web app renders top-to-bottom
# Title needs to be specified for before and after prediction
# (Otherwise prediction output will display above Title)

# Importing Important Libraries
import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

# Setting-up Streamlit Web Page Configuration
st.set_page_config(page_title='Protein Structure Prediction using ESMFold')


# Formatting Streamlit Webpage using CSS Style
st.markdown("""
<style>
body {
    background-color: #F7F7F7;
    font-family: "Open Sans", sans-serif;
}

h1 {
    font-size: 48px;
    text-align: center;
    font-weight: bold;
    margin-top: 40px;
}


h3 {
    font-size: 48px;
    text-align: center;
    font-weight: bold;
    margin-top: 40px;
}

.container {
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0px 0px 10px #BBBBBB;
    margin-top: 80px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.sidebar {
    width: 250px;
    height: 500px;
    border-radius: 20px;
    margin-top: 80px;
    box-shadow: 0px 0px 10px #BBBBBB;
    padding: 20px;
    text-align: center;
}

.sidebar select, .sidebar textarea {
    width: 200px;
    height: 40px;
    border-radius: 20px;
    font-size: 18px;
    padding: 10px;
    margin-top: 20px;
    border: none;
}

.sidebar .checkbox {
    margin-top: 20px;
    font-size: 18px;
}

#mol-div {
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# base\app.py

## User Input for Protein Sequence

# Example Protein Sequences

PROTEIN_1 = "PETase"
PROTEIN_2 = "Neuraminidase"
PROTEIN_3 = "Ubiquitin-D77"

PROTEIN_1_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
PROTEIN_2_SEQ = "VKLAGNSSLCPINGWAVYSKDNSIRIGSKGDVFVIREPFISCSHLECRTFFLTQGALLNDKHSNGTVKDRSPHRTLMSCPVGEAPSPYNSRFESVAWSASACHDGTSWLTIGISGPDNGAVAVLKYNGIITDTIKSWRNNILRTQESECACVNGSCFTVMTDGPSNGQASYKIFKMEKGKVVKSVELDAPNYHYEECSCYPNAGEITCVCRDNWHGSNRPWVSFNQNLEYQIGYICSGVFGDNPRPNDGTGSCGPVSSNGAYGVKGFSFKYGNGVWIGRTKSTNSRSGFEMIWDPNGWTETDSSFSVKQDIVAITDWSGYSGSFVQHPELTGLDCIRPCFWVELIRGRPKESTIWTSGSSISFCGVNSDTVGWSWPDGAELPFTIDK"
PROTEIN_3_SEQ = "ATGCAGATCTTCGTCAAGACGTTAACCGGTAAAACCATAACTCTAGAAGTTGAACCATCCGATACCATCGAAAACGTTAAGGCTAAAATTCAAGACAAGGAAGGCATTCCACCTGATCAACAAAGATTGATCTTTGCCGGTAAGCAGCTCGAGGACGGTAGAACGCTGTCTGATTACAACATTCAGAAGGAGTCGACCTTACATCTTGTCTTAAGACTAAGAGGTGGTGACTGA"

# Side Bar Set-Up
selected_protein = st.sidebar.selectbox("Select a protein example", (PROTEIN_1, PROTEIN_2, PROTEIN_3))

if selected_protein == PROTEIN_1:
    txt = st.sidebar.text_area('or Input Protein Sequence', PROTEIN_1_SEQ, height=275, max_chars=400)
elif selected_protein == PROTEIN_2:
    txt = st.sidebar.text_area('or Input Protein Sequence', PROTEIN_2_SEQ, height=275, max_chars=400)
else:
    txt = st.sidebar.text_area('or Input Protein Sequence', PROTEIN_3_SEQ, height=275, max_chars=400)

style = st.sidebar.selectbox('style',['cartoon','line','stick','sphere'])
spin = st.sidebar.checkbox('Spin', value = False)


# Visual for Predicted Protein Structure
def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({style:{'color':'spectrum'}})
    pdbview.setBackgroundColor('black')
    pdbview.zoomTo()
    pdbview.zoom(2, 1000)
    if spin:
        pdbview.spin(True)
    else:
        pdbview.spin(False)
    showmol(pdbview, height = 500,width=1000)

# Calling ESMFold API for Protein Structure Prediction
# Generating PDB File
# Displaying Prediction
# Calculating pLDDT Confidence
def update(sequence=txt):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence)
    name = sequence[:3] + sequence[-3:]
    pdb_string = response.content.decode('utf-8')

    # Write PDB File
    with open('predicted.pdb', 'w') as f:
        f.write(pdb_string)

    # Calculate pLDDT Score
    struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
    b_value = round(struct.b_factor.mean(), 4)

    # Webpage Title
    with st.container():
        st.title('Protein Structure Prediction using ESMFold')
        st.write(
            '[*ESMFold*](https://esmatlas.com/about) is an end-to-end single sequence protein structure predictor based on the ESM-2 language model. For more information, read the [research article](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) and the [news article](https://www.nature.com/articles/d41586-022-03539-1) published in *Nature*.')

    # Prediction Container
    with st.container():

        # Display protein structure
        st.subheader('Visualization of predicted protein structure')
        render_mol(pdb_string)


        # plDDT value is stored in the B-factor field
        st.subheader('plDDT')
        st.write('plDDT is a per-residue estimate of the confidence in prediction on a scale from 0-100.')
        st.info(f'plDDT: {b_value}')

        # Option to download PDB file for user
        st.download_button(
            label="Download PDB",
            data=pdb_string,
            file_name='predicted.pdb',
            mime='text/plain',
        )

# When predict is clicked; Display: Predicted Structure and pLDDT score
predict = st.sidebar.button('Predict', on_click=update)
# Signature
st.sidebar.subheader('This app was developed by Shaheer Syed')

# Default homepage when prediction not requested
if not predict:
    # Generate Title Again (Read Note Above)
    st.title('Protein Structure Prediction using ESMFold 🧬')
    st.write(
        '[*ESMFold*](https://esmatlas.com/about) is an end-to-end single sequence protein structure predictor based on the ESM-2 language model. For more information, read the [research article](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) and the [news article](https://www.nature.com/articles/d41586-022-03539-1) published in *Nature*.')

    # Note to user
    st.warning('⬅ Enter protein sequence data!')