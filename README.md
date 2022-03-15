[![build](https://github.com/shyamal-anadkat/AIPI540_NLP/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/shyamal-anadkat/AIPI540_NLP/actions/workflows/main.yml)

# Mood & Movies <br/>
> Better movie recommendations, based on your mood
#### AIPI 540 NLP Team Project | Spring Semester 2022

**Team Members:** Shyamal Anadkat, Hearsch Jariwala, Snigdha Rudraraju

**Project:** Building NLP based movie recommendation web application based on mood & user query/free text input. 

## Getting Started

Run the Streamlit interface from root of the project: `streamlit run app.py`
- Note the pre-loading would take ~2mins on CPU but after the pre-loading the recommendation search would be quick.

## Project Structure 

```
├── README.md               <- description of project and how to set up and run it
├── requirements.txt        <- requirements file to document dependencies
├── Makefile                <- setup and run project from command line
├── app.py                  <- main script to run user interface
├── scripts                 <- directory for pipeline scripts or utility scripts (see scripts/README.md)
├── models                  <- directory for trained model
├── data                    <- directory for project data
    ├── raw                 <- directory for raw data or script to download
    ├── processed           <- directory to store processed data
    ├── outputs             <- directory to store any output data
├── notebooks               <- directory to store any exploration notebooks used
├── .gitignore              <- git ignore file
```
Documentation for [scripts](https://github.com/shyamal-anadkat/mood-n-movies/blob/master/scripts/README.md)

## Contributing 

* Run `make clean` before pushing your code (which will format and do the linting for you)
* Please ensure the build on github passes after you merge your code to master/push your commit 

