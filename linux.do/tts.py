from openai import OpenAI

key = "eyJhbGkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcxMjQ3NDk1MSwiZXhwIjoxNzEzMzM4OTUxLCJhenAiOiJwZGxMSVgyWTcyTUlsMnJoTGhURTlWVjliTjkwNWtCaCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9mZmxpbmVfYWNjZXNzIn0.RctLHH1fRmBmpsZMLKxHQZnVnZYuHa8HB3Fe36qlfWOSj-_jAvwU_wCgEZiPYBO8Poc3OWSG0u1I8rzIuKhxje3CUfXT-OiC5qdfDP8TpjhbDNB7xjoCahy-TFh7TeKoQuv94nHkWEHOWFqs_0xXNeHeHW6kccchJaBNAJHY6jHdfKwhpgwwWEc7c8edQbao4I53kPDfrJ1iA1ii7NrR0y7HDhO7E2qbqS3JVe7DeMyw7OMEOFaPz4pmTNU4ZGKzfHzQdsCXkHRtuBiff7wa5d7EEn7dNTBYNFmBX_YI5DkJl-maOKfga84pZP-yNEi6kOR5NdowYqA8selqkkl6Ow"
base_url = "https://api.oaifree.com/v1"
# 从文件中读取文本
with open('input_text.txt', 'r', encoding='utf-8') as file:
    input_text = file.read()

# 初始化客户端
client = OpenAI(
    api_key=key,
    base_url=base_url
)
# Experiment with different voices (alloy, echo, fable, onyx, nova, and shimmer) to find one that matches your desired tone and audience. The current voices are optimized for English.
# 调用语音合成API，使用读取的文本作为输入
response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input=input_text
)

# 将生成的语音保存为MP3文件
response.stream_to_file("output.mp3")
