import streamlit as st
from openai import OpenAI
import os
from io import BytesIO
from byaldi import RAGMultiModalModel
from PIL import Image
import base64
import time

# Set up token
token = os.environ["GITHUB_TOKEN"]

def extract_topic(user_input, model_name, openai_client):
    """
    Extract a concise topic or key phrase from the user's query using an LLM.
    """
    extraction_prompt = (
        "You are an assistant that extracts the main topic from a user's question. "
        "Reply ONLY with the concise topic, without any explanation or extra text. "
        " For example query: generate questions for segmentation methods for nuclei - would lead to topic: segmentation methods for nuclei"
        f"Query: {user_input}"
    )
    response = openai_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You extract concise topics from user questions."},
            {"role": "user", "content": extraction_prompt},
        ],
    )
    extracted_topic = response.choices[0].message.content.strip()
    return extracted_topic


def generate_quiz(user_topic:str, model, num_slides = 4, num_questions = 2):
    """
    Generate a set of exam-like questions, when asked for it, based on the required topic. First, Slides are fetched from the database that best match to the topic. 
    Second, those slides are used to formulate some exam-like questions that refer to the slides content, i.e. the desired topic from the user input.
    """

    endpoint = "https://models.github.ai/inference"
    client = OpenAI(base_url=endpoint,api_key=token)
    
    # Load the RAG model
    docs_retrieval_model = RAGMultiModalModel.from_index("BIDS_index", device="cpu")

    # Retrieve k best results
    results = docs_retrieval_model.search(user_topic, k=num_slides)

    # Reconstruct the Images from the resulting Slides
    reconstructed_images = []
    
    for result in results:
        base64_img = result["base64"]  
        image_data = base64.b64decode(base64_img)
        image = Image.open(BytesIO(image_data))
        reconstructed_images.append(image)
    
    system_prompt = "You are a skilled AI assistant that analyzes slide presentations and creates a set of Exam Questions from them. Output only the Questions, not possible anwsers. Don't refer to the slides in your questions."
    prompt = (
    f"Take a look at the Slide and suggest Exam Questions concerning the topic: {user_topic}. "
    f"Output exactly {num_questions} questions. Questions should be able to be answered with the help of the slides. "
    f"Be aware that certain slides show questions themselves (marked by hands with colorful cards) — try not to interpret those questions, but rather just take the questions as they are or skip those slides."
    ) 
    
    # Build image inputs
    image_inputs = [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{result['base64']}"}} for result in results]

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [
            {"type": "text", "text": prompt},
            *image_inputs  
        ]}
    ]
    
    # Send request
    response = client.chat.completions.create(model=model, messages=messages)
    
    # Store response
    reply = response.choices[0].message.content

    return reply, reconstructed_images
    

def main():
    # Set your OpenAI API key (or use environment variable)
    endpoint = "https://models.github.ai/inference"
    client = OpenAI(base_url=endpoint,api_key=token)
    
    # title
    st.title("💬 SlideInsight Chatbot for the Bio-Image Data Science Lecture")
    st.markdown("Explore Presentation Slides from the [BIDS lecture 2025](https://zenodo.org/records/15698366) (authored by Robert Haase).")
    
    # sidebar
    with st.sidebar:

        if st.button("🔄 Reset Chat"):
            st.session_state.messages = []
            st.session_state.images = []  # reset images too
            st.success("Chat reset!")

        st.markdown("Reset has to be done after changing variables from the SlideBar")
        st.markdown("##")
        
        st.title("Trigger Words:")
        st.markdown("To trigger the **creation of questions** use one of the following words in your query:")
        st.markdown("_quiz, generate, exam, questions, exam-like, question_")
        st.markdown("To trigger the model to **show the relevant slides** for the current topic use one of the following words in your query:")
        st.markdown("_images, image, slide, slides_")
        
        st.markdown("##")
        st.markdown("##")
        # radio button for model choice
        available_models = ["openai/gpt-4.1", "openai/gpt-4o", "openai/gpt-4.1-mini", "openai/gpt-4o-mini"]
        model_name = st.radio('Choose a model', available_models, index=0)  # index=0 sets default
        
        st.markdown("##")
        st.markdown("##")

        # Number of slides selector
        num_slides = st.slider('Number of slides to fetch for each topic (Default: 4)', min_value=1, max_value=20, value=4)
        
        # Number of questions selector
        num_questions = st.slider('Number of questions to generate for each topic (Default: 2)', min_value=1, max_value=20, value=2)

        st.markdown("##")
        st.markdown("##")
        st.title("Additional Information")
        st.markdown("For more Information about the Slides please visit the [Github Page](https://github.com/ScaDS/SlideInsights-for-BIDS-lecture-25) Website.")
        
    # Initialize Welcome Message
    if 'welcome_shown' not in st.session_state:
        st.session_state.welcome_shown = True
        st.markdown("##")
        st.markdown("##")
        st.markdown("##")
        st.markdown("##")
        st.markdown("### 👋 Hello there!")
        st.markdown("Use the trigger words found in the sidebar on the left to let the model generate questions about the lecture and show you the corresponding slides.")

    # Initialize chat history
    if "messages" not in st.session_state or not st.session_state.messages:
        system_prompt = (
        "You are a helpful AI assistant in a chat interface.")
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
    
    # Display previous messages
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    # Input box for user Text
    user_input = st.chat_input("Enter your Question ...")
    
    if user_input:
        # Store user's message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Question generation
        if (
            any(trigger in user_input.lower() for trigger in ["quiz", "generate", "exam", "questions", "exam-like", "question" ]) and
            not any(trigger in user_input.lower() for trigger in ["images", "image", "slide", "slides"])
        ):
            with st.chat_message("assistant"):
                with st.spinner("Generating Questions ... "):
                    try:
                        topic = extract_topic(user_input, model_name, client)
                        st.markdown(f"**Detected Topic:** {topic}")
                        reply, images = generate_quiz(topic, model_name, num_slides, num_questions)

                        st.session_state.images = images  # store images persistently
                        st.markdown(reply)

                        st.session_state.messages.append({"role": "assistant", "content": reply})
                        
                    except Exception as e:
                        st.error(f"Error processing file: {e}")
                        assistant_reply = "Sorry, I couldn't process query. Do you want me to generate exam-like questions or to show you the slides from your last set of questions?"
                        st.markdown(assistant_reply)
                        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})


        # Slide presentation
        elif (
            any(trigger in user_input.lower() for trigger in ["images", "image", "slide", "slides"]) and
            not any(trigger in user_input.lower() for trigger in ["quiz", "generate", "exam", "questions", "exam-like", "question" ])
        ):
            with st.chat_message("assistant"):
                with st.spinner("Fetching relevant slides ..."):
                    try:
                        if "images" in st.session_state and st.session_state.images:
                            st.markdown("### Related Slides:")
                            for img in st.session_state.images:
                                st.image(img, use_container_width=True)
                            assistant_reply = "Here are the slides related to your last topic."
                            st.markdown(assistant_reply)
                            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                        else:
                            assistant_reply = "Sorry, I don't know the topic yet. Please generate questions first so I can fetch the relevant slides."
                            st.markdown(assistant_reply)
                            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

                    except Exception as e:
                        st.error(f"Error processing file: {e}")
                        assistant_reply = "Sorry, I couldn't process query. Do you want me to generate exam-like questions or to show you the slides from your last set of questions?"
                        st.markdown(assistant_reply)

        # Trigger words for both
        elif (
            any(trigger in user_input.lower() for trigger in ["images", "image", "slide", "slides"]) and
            any(trigger in user_input.lower() for trigger in ["quiz", "generate", "exam", "questions", "exam-like", "question" ])
        ):
            with st.chat_message("assistant"):
                        assistant_reply =  "Please use only trigger words for either questions generation OR presentation of slides. You can find the corresponding trigger words on the left."
                        st.markdown(assistant_reply)
                        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            
        # No trigger words                
        else:
            with st.chat_message("assistant"):
                    with st.spinner("No trigger words found. Preparing fallback response ..."):
                        fallback_response = client.chat.completions.create(model=model_name, messages=st.session_state.messages)
                        assistant_reply =  fallback_response.choices[0].message.content
                        time.sleep(3)  # keep spinner visible for at least 4 seconds
                        st.markdown(assistant_reply)
                        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    


if __name__ == "__main__":
    main() 
