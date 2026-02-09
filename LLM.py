from google import genai

client = genai.Client(
    api_key="AIzaSyAwckPwImB4dw0yma3AI2IhG_rtZBS6R-4"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)
