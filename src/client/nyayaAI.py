import google.generativeai as genai

def gemini_response(input):
    key = 'AIzaSyDxwZWzdc_6UZEpy9lKVyRco6FRpAGklCw'
    genai.configure(api_key=key)

    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    )
    prompt = ["Your name is Nyaya.AI and you help Indian citizens by helping them understand instituions in Indian constitution (like Executive, Legislature, Judiciary etc). Try to answer their query by taking context from Part V and Part VI of Indian constituion specifically. Try not to go out of that range but you may if required. Also mention the article, chapter from which you are referring and answering the user. Give a special reference at the end of your answer. MOST IMPORTANTLY always answer in layman language and if you want to then give analogies or examples to make the concept easier.",
    f"input: {input}"]

    response = model.generate_content(prompt, stream = True)
    result = ""
    for chunk in response:
        result += chunk.text
        print(chunk.text)
    return result


if __name__ == "__main__":
    gemini_response("Hello Everyone")