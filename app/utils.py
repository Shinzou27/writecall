import requests

url = lambda endpoint: f"http://127.0.0.1:8000/api/{endpoint}"
call_id = 0
headers = {'Content-Type': 'application/json'}
def set_call_id(id):
  global call_id
  call_id = id
  print(f"call id que acabei de botar: {call_id}")
import requests

def post_audio(audio_file):
    global call_id
    print(f"call id: {call_id}")
    
    if call_id >= 1:
        files = {'audio_file': audio_file}
        data = {'call_id': call_id}
        try:
            response = requests.post(url("audio"), data=data, files=files)
            try:
                res_json = response.json()
                return res_json['id']
            except ValueError:
                print("Resposta não é JSON, conteúdo bruto:")
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar requisição: {e}")
        



def post_transcription(audio_chunk_id, text):
  if audio_chunk_id >= 1:
    try: 
      transcription = requests.post(url("transcription"), json={"audio_chunk_id": audio_chunk_id, "text": text})
      try:
          return transcription
      except ValueError:
          print("Resposta não é JSON, conteúdo bruto:")
          print(transcription.text)
    except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar requisição: {e}")