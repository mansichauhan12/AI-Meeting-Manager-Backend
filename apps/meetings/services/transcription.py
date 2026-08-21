from .ai_client import GeminiClient


class TranscriptionService:

    @staticmethod
    def transcribe(audio_file_path):

        client = GeminiClient().get_client()

        # Upload the file to Gemini
        audio_file = client.files.upload(file=audio_file_path)

        # Generate content
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=[
                "Transcribe this audio file accurately. Please only output the transcript.",
                audio_file
            ]
        )
        
        # Cleanup the file from Gemini storage
        client.files.delete(name=audio_file.name)

        return response.text