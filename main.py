from fastapi import FastAPI, UploadFile, File
from openai import OpenAI
import io
import json

app = FastAPI()
client = OpenAI(api_key="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")


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    
    # Save the file to the current folder
    with open(file.filename, 'wb') as f:
        f.write(contents)

    audio_file = open("datascience.mp3", "rb")
    transcript = client.audio.translations.create(
        model="whisper-1", 
        file=audio_file
    )

    summarize = transcript.text

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "Please give the summary of this online class in json format, and 'title', 'summary', 'topics_dicussed','point_to_remember' in json format make sure to give topics_discussed and point_to_remember in text only in 50 words"},
            {"role": "user", "content": summarize}
        ]
    )

    # Get the content from the response
    content = response.choices[0].message.content

    # Remove the markdown code block identifiers
    content = content.replace("```json\n", "").replace("\n```", "")

    # Convert the string to a JSON object
    json_response = json.loads(content)

    print(json_response)
    return json_response
