#!/usr/bin/env python3
import os
import requests


async def chat(ctx, prompt):

    params = {
        'model': 'gpt-3.5-turbo',
        'messages': [{"role": "system", "content": "You are a relaxed, sarcastic, and funny friend."},
                     {'role': 'user', 'content': prompt}],
        'user': ctx.user.id
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': str(os.getenv('OPENAI_TOKEN')),
    }

    await ctx.respond(content='*⏳ Loading...*')

    r = requests.post('https://api.openai.com/v1/chat/completions',
                      json=params, headers=headers).json()

    response = r['choices'][0]['message']['content']

    await ctx.edit(content=f'{response}')
