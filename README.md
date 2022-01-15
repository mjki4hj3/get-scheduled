# Get Scheduled

---
## How to setup

1. Clone or fork into your local repository

2. Install pipenv if you don't already have it

```bash
pip install pipenv
```

3. Add your course list in the data folder. Note: you must use the exact column headers and name the file src-data.xlsx


3. Create virtual python environment and install dependencies
```bash 
pipenv shell && pipenv install 
```

4. Setup [Google OAuth Credentials](https://developers.google.com/workspace/guides/create-credentials?authuser=3#oauth-client-id) and add the credentials.json file into the project root. Make sure to set the uri to http://localhost:5000/ 

5. To run the application from the root directory

```bash
cd calendar && python quickstart.py
```

6. When you first run the application approval needs to be given to the app
---
## Project Aims

- Have fun
- Solve a real-world problem using Python
- Gain practical experience in using collaborative tools such as GitHub and Trello 

## Project Objectives:
- Create a schedule that serves as a guide for when to study and when to take breaks
- The app takes in a course list (excel or csv) with duration of each topic (in this case a video course), as shown in Table 1, and outputs a study schedule based on parameters inputted by the user (e.g. study duration/day, break duration etc).

<p align='center'><img src=images/Tables.jpeg width=300px height= 336px></p>

- Outputted study schedule then gets automatically put into your Google Calendar via an API call

## Current Outputs

- Excel schedule outputed based on a [pomodoro split](https://www.youtube.com/watch?v=1pADI_eZ_-U) of 45 minutes of study and 15 minutes break

<p align='center'><img src=images/outputted-study-schedule.png width=1952px height= 916px></p>

- Calendar events that were inserted based on above study schedule

<p align='center'><img src=images/google-calendar-schedule.jpeg width=500px height= 636px></p>

## Future Works
- Current ongoing and future developments of this project can be seen detailed in the milestones tab

## Resources

### Setup

[Pipenv Guide - Virtual Environment & Package Management](https://realpython.com/pipenv-guide/)

[Google Calendar - Python Installation](https://developers.google.com/calendar/api/quickstart/python)

[Google Calendar API - OAuth Credentials Setup](https://developers.google.com/workspace/guides/create-credentials?authuser=3#oauth-client-id)


### Project Development

[Pandas Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)

[Pandas Tutorials](https://pandas.pydata.org/pandas-docs/stable/getting_started/tutorials.html)

[Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

### Information

[What is the pomodoro study technique?](https://www.youtube.com/watch?v=1pADI_eZ_-U)