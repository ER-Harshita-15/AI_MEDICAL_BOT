import os
import gradio as gr
from brain_of_doctor import encode_image, analyze_image_with_query
from voice_of_patient import transcribe_with_groq
from voice_of_doctor import text_to_speech_with_elevenlabs

# System prompt for the AI doctor
system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    try:
        # 1. Transcribe audio
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )

        # 2. Analyze image with transcribed query
        if image_filepath:
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_to_text_output,
                encoded_image=encode_image(image_filepath),
                model="llama-3.2-11b-vision-preview"
            )
        else:
            doctor_response = "No image provided for me to analyze."

        # 3. Generate voice reply
        output_voice_path = text_to_speech_with_elevenlabs(
            input_text=doctor_response,
            mp3_filepath="final.mp3",
            wav_filepath="final.wav"
        )

        return speech_to_text_output, doctor_response, output_voice_path

    except Exception as e:
        return str(e), str(e), None


iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Speak to Doctor"),
        gr.Image(type="filepath", label="Upload Affected Area Image")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(type="filepath", label="Voice Reply from Doctor")
    ],
    title="AI Doctor with Vision and Voice",
    description="Talk to the doctor, upload a medical image, and hear back what the AI thinks!"
)

iface.launch(debug=True)

#http://127.0.0.1:7860