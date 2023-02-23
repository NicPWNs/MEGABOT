async def chat(ctx, prompt):

    params = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 4000,
        'temperature': 1,
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': str(os.getenv('OPENAI_TOKEN')),
    }

    await ctx.respond(content="*⏳ Loading...*")

    r = requests.post("https://api.openai.com/v1/completions",
                      json=params, headers=headers).json()

    response = r["choices"][0]["text"]

    await ctx.edit(content=f"{response}")
