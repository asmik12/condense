import openai
import json

with open('winning_projects.json', 'r') as file:
    data = json.load(file)

prompts = []
for item in data:
    prompt = "Generate a 1 sentence summary of a project with title {item['title'] given the following information about what it does : {item['what_it_does']}'}"
    prompts.append(prompt)

#Set API Key

openai.api_key = "SOMEKEY" #secret key - lahacks

responses = []
for prompt in prompts:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"user",
             "content": prompt}
        ], 
        max_tokens = 50
    )
    summary = response.choices[0].message['content']
    responses.append(
        {
            "title": item['title'], 
            "summary": summary
        }
    )

with open('summaries.json', 'w') as outfile:
    json.dump(responses, outfile)

print("Project summaries saved to summaries.json")