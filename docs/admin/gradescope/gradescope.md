# Building an Autograder for Gradescope

## Grading procedure 

The LLM grader application also provides a simple method to build autograders for Gradesccope.
The general flow is:

- Students answer questions on LLM grader portal for a particular unit
- Students are allowed an infinite number of tries until they get all questions correct
- Students then go to the Dashboard and then select **Download Submission**.  This
selection will create a JSON file submission.
- Students go to Gradescope and upload the submission.
- The autograder app will verify that the questions are correct.

Importantly, the autograder app on Gradescope.  It simply reads the results from the LLM grader.
It makes no calls to OpenAI or perform any processing.

## Building the Gradescope Autograder

To build the Gradescope autograder:

- Navigate to the location for unit XML file, say `unit1_basic_logic.xml`.
- Activate the virtual environment with `llmgrader` in a terminal
- Run

```bash
build_autograder --schema unit1_basic_logic.xml
```

or whatever your unit name is.

- This command creates a file `autograder.zip`

## Creating the Gradescope assignment

Now go to Gradescope

- Select your course and go to **Assignments**
- Select **Create Assignment** (bottom right)
- Select **Programming Assignment** and fill in the standard information such as name, due data
    - For **Autograder Points** select the total number of points for the unit.
    This value will be sum of all the points in the units for the required questions
    - Uncheck **manual grading** since we will be completely grading the assignment automatically
- On the **Configure autograder** page:
   - For **autograder configuration** select **zip file upload**
   - Select the autograder file, `autograder.zip` created in the previous step
   - Select **Update Autograder**.  
   - The Autograder will now take a minute or two to build
   - If you have a JSON file submission, you can test it now.  Otherwise, go to the next step

## Testing the Autograder

To test the autograder:

- Go back to the AI grader portal on render
- Answer some or all of the questions that are required for the unit
- Go the **Dashboard** and then select **Download sumbission**.  This selection will create a JSON submission
- Go back to the Assignment in Gradescope
- Select **Configure Autograder**.  Select **Test autograder**.  Then, upload the JSON submission
