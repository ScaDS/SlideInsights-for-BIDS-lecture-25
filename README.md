# Slide Insights for the BIDS Lecture 2025 
This repository helps preparing for the [BIDS lecture 2025](https://zenodo.org/records/15698366) (authored by Robert Haase) exam by generating exam-like questions and searching for the corresponding slides in the slide deck from the lecture.




### Before getting started
To access the VLM used in this repository, this [free Service from Github](https://github.com/marketplace/models) is used.

***Be aware that there are certain [rate limits](https://docs.github.com/en/github-models/prototyping-with-ai-models#rate-limits) for each model!***

Make sure to generate a developer key / personal access token on Github and set it as an environment variable. You can generate the token via the [Github website](github.com) under user settings and afterwards set it like this for your current session:


##### bash:
```export GITHUB_TOKEN= "your-github-token-goes-here"```

##### powershell:
```$Env:GITHUB_TOKEN= "your-github-token-goes-here"```

##### Windows command prompt:
```set GITHUB_TOKEN= your-github-token-goes-here```


### Create a conda environment
Code was only tested for Python 3.10.12. To run the code, you have to re-create the conda/ virtual environment. Create a new one and install all packages with

##### bash:
```pip install -r requirements.txt```




### Notebooks
#### [1_Download_Slides](1_Download_Slides.ipynb)
Downloads all PDF files from the [BIDS lecture 2025](https://zenodo.org/records/15698366) authored by Robert Haase and licensed under CC-BY-4.0. 



#### [2_Index_Slides](2_Index_Slides.ipynb)
Creates and saves an index to search for Slides that best match to a text query.For this, the [byaldi](https://github.com/AnswerDotAI/byaldi) package is used. 

It uses [poppler](https://poppler.freedesktop.org/) under hood, which also has to be installed in order to make this work. 

##### bash:
```sudo apt-get install -y poppler-utils```

##### conda:
```conda install -c conda-forge poppler```



#### [3_Generate_Questions](3_Generate_Questions.ipynb)
A query with the desired question topic is sent to the RAG Model to fetch some slides with similar contents. These slides are then passed to the VLM to generate the questions.

To check whether one could answer correctly, the slides can then be reconstructed and visualized.





To cite the material used in this repository you can use the following citation:
Haase, R. (2025, June 19). Bio-image Data Science Lectures 2025 @ Uni Leipzig / ScaDS.AI. Zenodo. https://doi.org/10.5281/zenodo.15698366
