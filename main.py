#uvicorn fastapi_app:app --reload

from fastapi import FastAPI, Form, Request, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

# Create a list to store submissions
# submissions = []

# Dictionary to store form submissions
form_submissions = {}

class FormData(BaseModel):
    data: dict

@app.post("/submit/{form_id}/")
async def submit(request: Request,  form_id: int):
    # Parse the form data into a dictionary
    form_data = await request.form()
    form_data_dict = {field: form_data[field] for field in form_data}


     # Check if the form_id exists in the dictionary, create it if not
    if form_id not in form_submissions:
        form_submissions[form_id] = []

    # Append the form data to the form_id
    form_submissions[form_id].append(form_data_dict)

    # Save the serialized form data to a file (if needed)
    with open(f"form_data_{form_id}.json", "w") as f:
        f.write(json.dumps(form_data_dict))


    # Store the form data in the submissions list
    # submissions.append(form_data_dict)

    # Save the serialized form data to a file.
    # with open("form_data.json", "w") as f:
    #     f.write(json.dumps(form_data_dict))

    first_name = "First Name2"

    # Generate a unique index for this submission
    # submission_index = len(submissions) - 1

    # Return the form HTML after processing (an empty form)
    return f"""
    <html>
    <body>
        <form action="/submit/{form_id}/" method="post">
            {"".join(f"<label for='{field}'>{field}:</label><br><input type='text' id='{field}' name='{field}'><br><br>" for field in form_data_dict)}
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """





# Redirect to the form page after processing
# return RedirectResponse(url="/form")

@app.get("/form")
async def get_form():
    # Return the HTML form page where users can enter new data
    return """
    <html>
    <body>
        <form action="/submit/" method="post">
            <label for="fname">First Name:</label><br>
            <input type="text" id="fname" name="fname"><br><br>
            <label for="lname">Last Name:</label><br>
            <input type="text" id="lname" name="lname"><br><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """


# @app.post("/submit", response_model=FormData)
# async def submit(form_data: UploadFile):
#     print('DDD', form_data)
#     # Parse the multipart/form-data request.
#     parser = FormDataParser(form_data.file)
#     form_data_dict = parser.parse()

#     # Convert the form data to a FormData object.
#     form_data = FormData(**form_data_dict)

#     # Submit the form data.
#     await submit_form_data(form_data)

#     return form_data

@app.get("/retrieve")
async def get_form_data(index: int):
    # Load the serialized form data from the file.
    file_name = f"form_data_{index}.json"  # Use the index to generate the file name.

    try:
        with open(file_name, "r") as f:
            json_data = f.read()
            if not json_data:
                return {"error": "No data found for the specified index."}
        # Deserialize the serialized form data.
        form_data = json_data #FormData(**json.loads(json_data))
        return form_data
    except FileNotFoundError:
        return {"error": "Data not found for the specified index."}
    except json.JSONDecodeError as e:
        return {"error": f"Error decoding JSON data: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}



# @app.get("/retrieve")
# async def get_form_data():
#     # Load the serialized form data from the file.    

#     print('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
#     with open("form_data.json", "r") as f:
#         json_data = f.read()

#         print('data: .....', json_data)

#     # Deserialize the serialized form data.
#     form_data = FormData(**json.loads(json_data))

#     return form_data    