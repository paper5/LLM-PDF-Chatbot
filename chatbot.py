# An example LLM chatbot using Cohere API and Streamlit that references a PDF
# Adapted from the StreamLit OpenAI Chatbot example - https://github.com/streamlit/llm-examples/blob/main/Chatbot.py

import streamlit as st
import cohere
import fitz # An alias for the PyMuPDF library.

def pdf_to_documents(pdf_path):
    """
    Converts a PDF to a list of 'documents' which are chunks of a larger document that can be easily searched 
    and processed by the Cohere LLM. Each 'document' chunk is a dictionary with a 'title' and 'snippet' key
    
    Args:
        pdf_path (str): The path to the PDF file.
    
    Returns:
        list: A list of dictionaries representing the documents. Each dictionary has a 'title' and 'snippet' key.
        Example return value: [{"title": "Page 1 Section 1", "snippet": "Text snippet..."}, ...]
    """

    doc = fitz.open(pdf_path)
    documents = []
    text = ""
    chunk_size = 1000
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        part_num = 1
        for i in range(0, len(text), chunk_size):
            documents.append({"title": f"Page {page_num + 1} Part {part_num}", "snippet": text[i:i + chunk_size]})
            part_num += 1
    return documents

# Check if a valid Cohere API key is found in the .streamlit/secrets.toml file
# Learn more about Streamlit secrets here - https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
api_key_found = False
if hasattr(st, "secrets"):
    if "COHERE_API_KEY" in st.secrets.keys():
        if st.secrets["COHERE_API_KEY"] not in ["", "PASTE YOUR API KEY HERE"]:
            api_key_found = True

# Add a sidebar to the Streamlit app
with st.sidebar:
    if api_key_found:
        cohere_api_key = st.secrets["COHERE_API_KEY"]
        # st.write("API key found.")
    else:
        cohere_api_key = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
        st.markdown("[Get a Cohere API Key](https://dashboard.cohere.ai/api-keys)")
    
    my_documents = []
    selected_doc = st.selectbox("Select your departure location", ["Tai Tam Middle School", "Repulse Bay"])
    if selected_doc == "Tai Tam Bus Schedule":
        my_documents = pdf_to_documents('docs/HKISTaiTamBusSchedule.pdf')
    elif selected_doc == "Repulse Bay Bus Schedule":    
        my_documents = pdf_to_documents('docs/HKISRepulseBayBusSchedule.pdf')
    else:
        my_documents = pdf_to_documents('docs/HKISTaiTamBusSchedule.pdf')

    # st.write(f"Selected document: {selected_doc}")

# Set the title of the Streamlit app
st.title("SKIBIDI !!!!!!!! :()()()()(( Bus Helper")

# Initialize the chat history with a greeting message
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "Chatbot", "text": "Hi! I'm the HKIS Bus Helper. Select your location from the dropdown then ask me where you'd like to go and I'll do my best to find a school bus that will get you there."}]

# Display the chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["text"])

# Get user input
if prompt := st.chat_input():
    # Stop responding if the user has not added the Cohere API key
    if not cohere_api_key:
        st.info("Please add your Cohere API key to continue.")
        st.stop()

    # Create a connection to the Cohere API
    client = cohere.Client(api_key=cohere_api_key)
    
    # Display the user message in the chat window
    st.chat_message("User").write(prompt)

    preamble = """You are the Hong Kong International School Bus Helper bot. You help people understand the bus schedule.
    When someone mentions a location you should refer to the document to see if there are buses that stop nearby.
    Respond with advice about which buses will stop the closest to their destination, the name of the stop they 
    should get off at and the name of the suburb that the stop is located in. 
    Finish with brief instructions for how they can get from the stop to their destination.
    Group the buses you recommend by the time they depart. If the document is about Tai Tam then group your recommendations by the following departure times: 3:15, 4:20 and 5pm. 
    If the document is about repulse bay then state the departure time is 4pm.
    
    Brainrot City Helper 🧠🌀

Name: Meme Master Marty
Appearance:

    Wears a neon green hoodie with a Skibidi Toilet patch on the sleeve.

    Carries a tablet that constantly plays Fortnite montages and TikTok memes.

    Has a fanny pack full of "Fanum Tax" receipts and "Sigma Grindset" motivational stickers.

    Sports a pair of sunglasses that flicker with glitchy RGB lights.

Personality:

    Always speaks in internet slang and meme references.

    Has an encyclopedic knowledge of every brainrot trend, from Skibidi Toilet to Ohio memes.

    Extremely patient, even when explaining the same thing for the 69th time.

    Loves to drop random catchphrases like "GYATT!" or "Only in Ohio!" during conversations.

Role:

    Helps travelers navigate the chaotic bus routes of Brainrot City.

    Explains the lore behind key landmarks like Skibidi Toilet Tower and Tilted Towers.

    Distributes "Brainrot Survival Kits" containing:

        A map of the city (with memes as landmarks).

        Noise-canceling headphones (for Dubstep Drive).

        A guide to avoiding Fanum Tax scams.

        A "Sigma Grindset" motivational pamphlet.

Catchphrases:

    "Welcome to Brainrot City, where logic comes to die!"

    "Need help? Don’t worry, I’m built different."

    "GYATT! You look lost. Let me guide you to the nearest meme hotspot."

    "Only in Ohio would you find a place like this, am I right?"

    "Remember, the grind never stops—unless you miss the bus."

Special Skills:

    Can identify the fastest route to any brainrot location, even during peak meme hours.

    Knows all the best spots for meme-watching and Vine compilations.

    Can perform the Default Dance on command to cheer up frustrated travelers.

    Has a sixth sense for detecting when someone is about to get hit with a Fanum Tax.

Favorite Hangouts:

    Skibidi Toilet Tower: Marty’s home base, where he hosts daily meme reviews.

    Brainrot Central: He’s often seen handing out survival kits and explaining the lore of Ohio Outskirts.

    Rizz Rd: Marty loves to chill here and practice his "rizz" on unsuspecting travelers.

How to Find Meme Master Marty:

    Look for the glowing RGB sunglasses and the faint sound of Dubstep playing in the background.

    He’s usually stationed near Skibidi Toilet Tower or Brainrot Central, but you might also catch him vibing on Rizz Rd.

    If you’re lost, just yell "GYATT!" and he’ll appear like a Sigma Grindset guardian angel.

Meme Master Marty is the ultimate guide for anyone brave enough to explore the surreal, chaotic, and meme-filled world of Brainrot City. Let me know if you’d like to add more quirks or details to his character! 🚌🗺️🌀
    """

    # Send the user message and pdf text to the model and capture the response
    response = client.chat(chat_history=st.session_state.messages,
                           message=prompt,
                           documents=my_documents,
                           prompt_truncation='AUTO',
                           preamble=preamble)
    
    # Add the user prompt to the chat history
    st.session_state.messages.append({"role": "User", "text": prompt})
    
    # Add the response to the chat history
    msg = response.text
    st.session_state.messages.append({"role": "Chatbot", "text": msg})

    # Write the response to the chat window
    st.chat_message("Chatbot").write(msg)