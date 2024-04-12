'''
Llama2 modules loaded and request behavior. 
'''

import ollama

MODEL = 'llama2'

def chat(msg):
    '''
    :param msg: User input in form of string
    :returns: Generator of various attributes from llama2 including the response
    '''
    #TODO: Make this process, blocking. Avoid spamming input
    stream = ollama.chat(
            model=MODEL,
            messages=[
                {'role': 'user', 'content': msg}
            ],
            stream=True,
    )

    for chunk in stream:
        if not chunk['done']:
            yield chunk['message']['content']
