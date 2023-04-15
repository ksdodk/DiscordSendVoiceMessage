import os, json
import requests


voice_data = open(os.getcwd() + "\\voice-message.ogg", "rb").read()

def data():
    file = json.load(open("config.json"))
    data = {
        "token":file["token"],
        "channel_id":file["channel_id"]
    }
    return data

json_data = data()

attach_url = f'https://discord.com/api/v10/channels/{json_data["channel_id"]}/attachments'
attach_headers = {
    'Content-Type': 'application/json',
    'Authorization': json_data["token"]
}
attach_data = {
    'files': [{
        'file_size': len(voice_data),
        'filename': 'voice-message.ogg',
        'id': '2'
    }]
}
attach_response = requests.post(attach_url, headers=attach_headers, data=json.dumps(attach_data))
attach_json = attach_response.json()
upload_url = attach_json['attachments'][0]['upload_url']
upload_filename = attach_json['attachments'][0]['upload_filename']

upload_headers = {'Content-Type': 'audio/ogg'}
print(requests.put(upload_url, headers=upload_headers, data=voice_data).text)

message_url = f'https://discord.com/api/v10/channels/{json_data["channel_id"]}/messages'
message_headers = {
    'Content-Type': 'application/json',
    'Authorization': json_data["token"],
    'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo5OTk5OTk5fQ=='
}
message_data = {
    'flags': 8192,
    'attachments': [{
        'id': '0',
        'filename': 'voice-message.ogg',
        'uploaded_filename': upload_filename,
        'duration_secs': 0.000001,
        'waveform': base64.b64encode(voice_data[:100]).decode("utf-8") 
    }]
}

print(requests.post(message_url, headers=message_headers, data=json.dumps(message_data)).status_code)
