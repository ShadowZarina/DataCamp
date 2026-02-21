"""
You'll create a chatbot using the OpenAI API to generate responses to the following Parisian tourist questions:

How far away is the Louvre from the Eiffel Tower (in miles) if you are driving?
Where is the Arc de Triomphe?
What are the must-see artworks at the Louvre Museum?
Create a list of dictionaries called conversation that lists the 'role' and 'content' for each question and response. You should start the conversation with a 'system' message to set the model's behavior, and use a temperature of 0.0 and maximum number of tokens of 100:
[ {"role": "system", "content": ...}, {"role": "user", "content": ...}, ... ]
"""

import os
from openai import OpenAI

# Define the model to use
model = "gpt-4o-mini"

# Define the client
client = OpenAI()

# Define the conversation
conversation =[
    {
        "role": "system",
        "content":"You are a travel guide designed to provide information about landmarks that tourists should explore in Paris. You speak in a concise manner."
    },
    {
        "role":"user",
        "content":"What is the most famous landmark in Paris?"
    },
    {
        "role":"assistant",
        "content":"The most famous landmark in Paris is the Eiffel Tower."
    },
]

# Define a list of questions
questions = [
    "How far away is the Louvre from the Eiffel Tower (in driving miles)?",
    "Where is the Arc de Triomphe?",
    "What are the must-see artworks at the Louvre Museum?",
]

# Loop through each question to generate responses
for question in questions:

    # Format the user input into dictionary form
    input_dict = {"role": "user", "content": question}
    
    # Add the user input dictionary to the conversation
    conversation.append(input_dict)  

    # Make the next API call
    response = client.chat.completions.create(
        model=model,
        messages=conversation,
        temperature=0.0,
        max_tokens=100
    )
    
    # Print the response from the model
    resp = response.choices[0].message.content
    print(resp)

    # Convert the response into the dictionary
    resp_dict = {"role": "assistant", "content": resp}
    
    # Append the response to the conversation
    conversation.append(resp_dict)


