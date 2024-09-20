from django.http import JsonResponse
from django.shortcuts import render
from openai import OpenAI;
import os

client = OpenAI(api_key='Your API KEY')

# Render the main chat page
def chat_view(request):
    return render(request, 'chat/chat.html')

# Process user messages using GPT-4
def gpt_response(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        gpt_message = response.choices[0].message.content
        return JsonResponse({"response": gpt_message})

# Whisper API to convert speech to text (simplified example
def whisper_view(request):
    if request.method == 'POST':
        try:
            if 'audio' not in request.FILES:
                return JsonResponse({"error": "No audio file provided"}, status=400)

            # Get the uploaded audio file
            audio_file = request.FILES['audio']

            # Define the save path in the current folder
            current_folder = os.path.dirname(os.path.abspath(__file__))  # Get current folder path
            save_path = os.path.join(current_folder, audio_file.name)

            # Save the audio file to the current folder
            with open(save_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            # Use the saved audio file for transcription
            with open(save_path, 'rb') as saved_audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=saved_audio_file
                )

            # Send the transcript back as a response
            return JsonResponse({"transcript": transcription.text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
