from gradio_client import Client

client = Client("hieuailearning/BAAI_bge_m3_api")
result = client.predict(text_input="Hello!!", api_name="/predict")
print(result)
