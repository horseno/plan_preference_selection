# plan_preference_selection
Annotation tool to collect preference of task plans with visulizations

# Setup:

1. Setup virtual env 
    ```
    #first time only
    conda create --name annotation python=3.9
    conda activate annotation
    ```
2. clone this repo
    ```
    # first time only
    git clone https://github.com/horseno/plan_preference_selection.git 
    cd plan_preference_select
    ```
    
3. Install required packages
    ```
    pip install -r requirements.txt #first time only 
    ```



4. Make sure the source csv file is in the `input` folder and modify environment vairable to point to the source file (defaults to input/pilot.csv)
```export DATA_FILE=input/pilot.csv```

5. Start the flask app
```python app.py```

6. Open http://127.0.0.1:5000 in the browswer

## Instructions:
**Task:** You'll be shown a sequence of pages showing independent tasks of performing pairwise comparisons of two logical plans given a conversation history between a user and an assistant agent. For Each row, read the conversation, select the better plan or "tie". 

## Aditional notes

**Input File:** defaults to `input/pilot.csv`, modify environment variable `DATA_FILE` to change.

**Output File:** selections will be automatically stored in the `output` directory, sharing prefix with the input file, ending with the system's username.  Your selection will be recorded with the corresponding row_id. Don't worry if you need to go back to change your selection, we'll take the later one if conflict exists.



