# Slide Insights for the BIDS Lecture 2025 
This repository helps preparing for the [BIDS lecture 2025](https://zenodo.org/records/15698366) (authored by Robert Haase) exam by generating exam-like questions and searching for the corresponding slides in the slide deck from the lecture.




### Before getting started
To access the VLM used in this repository, this [free Service from Github](https://github.com/marketplace/models) is used.

Be aware that there are certain [rate limits](https://docs.github.com/en/github-models/prototyping-with-ai-models#rate-limits) for each model!

Make sure to generate a developer key / personal access token on Github and set it as an environment variable. You can generate the token via the [Github website](github.com) under user settings and afterwards set it like this for your current session:


##### bash:
```export GITHUB_TOKEN= "your-github-token-goes-here"```

##### powershell:
```$Env:GITHUB_TOKEN= "your-github-token-goes-here"```

##### Windows command prompt:
```set GITHUB_TOKEN= your-github-token-goes-here```

**Optionally, you can also use local vision models, like [gemma3:4b](https://ollama.com/library/gemma3:4b) or [qwen2_5vl_3b](https://ollama.com/library/qwen2.5vl:3b). You can download them using [Ollama](https://ollama.com/).** 
Follow instructions on the Ollama Website (or from the [Course Material](https://github.com/ScaDS/BIDS-lecture-2025/blob/main/08a_llm_endpoints/02_ollama_endpoint.ipynb)) to download the models and get them running before executing the code from this repository.


### Create a conda environment
Code was only tested for Python 3.10.12. To run the code, you have to re-create the conda/ virtual environment. Create a new one and install all packages with

##### bash:
```pip install -r requirements.txt```




### Notebooks
#### [1_Download_Slides](1_Download_Slides.ipynb)
Downloads all PDF files from the [BIDS lecture 2025](https://zenodo.org/records/15698366) authored by Robert Haase and licensed under CC-BY-4.0. 



#### [2_Index_Slides](2_Index_Slides.ipynb)
Fetches pre-computed index files from [Zenodo](https://zenodo.org/records/15737931) and uses this index to match an example query to the lecture slides.

*OPTIONALLY:*
Creates and saves an index to search for slides that best match to a text query. For this, the [byaldi](https://github.com/AnswerDotAI/byaldi) package is used. 

It uses [poppler](https://poppler.freedesktop.org/) under hood, which also has to be installed in order to make this work. 

##### bash:
```sudo apt-get install -y poppler-utils```

##### conda:
```conda install -c conda-forge poppler```



#### [3_Generate_Questions](3_Generate_Questions.ipynb)
A query with the desired question topic is sent to the RAG Model to fetch some slides with similar contents. These slides are then passed to the VLM to generate the questions.

To check whether one could answer correctly, the slides can then be reconstructed and visualized.



### Streamlit App
The streamlit app is a simple chat interface to perform the task implemented in the [third Notebook](3_Generate_Questions.ipynb). You can trigger the model to generate exam-like questions to a certain topic (use one of the trigger words *quiz, generate, exam, questions, exam-like, question* in your query). Afterwards, you can take a look at the corresponding slided (use one of the trigger words *images, image, slide, slides*).

You can run the App using the Github Marketplace models with the following command:
##### bash:
```streamlit run streamlit_GitHub_models.py```

Alternatively, you can use local models and set the corresponding FLAG in the script first, then run:
##### bash:
```streamlit run streamlit_local_models.py```




### Citation
To cite the material used in this repository you can use the following citation:

Haase, R. (2025, June 19). Bio-image Data Science Lectures 2025 @ Uni Leipzig / ScaDS.AI. Zenodo. https://doi.org/10.5281/zenodo.15698366
