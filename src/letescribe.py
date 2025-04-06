import time, os, argparse, warnings
import whisper
from ollama import chat, ChatResponse

warnings.filterwarnings("ignore", category=UserWarning, module='whisper')

def save_transcript(transcript, file_path):
    """
    Saves the transcript to a text file.
    
    Parameters:
    transcript (list): A list of dictionaries containing audio metadata.
    file_path (str): The path to the output text file.

    Returns:
    transcript_str (str): The formatted transcript as a string.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        transcript_str = ""
        for segment in transcript['segments']:
            transcript_str += f"[{segment['start']:.2f} - {segment['end']:.2f}]: \t {segment['text']}\n"
        file.write(transcript_str)
        return transcript_str

def ask_ollama(transcript,ollama_model="llama3.1:8b") -> dict:
    """
    Sends the transcript to the ollama ai server and gets a JSON response. 

    Parameters:
    transcript (str): The transcript of the video.
    ollama_model (str): The model to be used for summarization (default=llama3.1:8b).
    """
    try:
        # response = AI.chat(
        #     model=ollama_model,
        #     messages=[{
        #         'role': 'user',
        #         'system':'You are a summarizing assistant responsible for analyzing the content of a meeting. The user will feed you transcriptions but you should always refer to the content in your response as "the video". Focus on accurately summarizing the main points and key details of the videos. Do not comment on the style of the video (e.g., whether it is a voiceover or conversational). Do never mention or imply the existence of text, transcription, or any written format. Use phrases like "The video discusses..." or "According to the video...". Strive to be the best summarizer possible, providing clear, and informative summaries that exclusively reference the video content.',
        #         'content': 'Transcript: ' + str(transcript)
        #         }],
        #     )
        response: ChatResponse = chat(model=ollama_model, messages=[
            {
                'role': 'user',
                'system':'You are a summarizing assistant responsible for analyzing the content of a presentation. I will feed you with transcriptions, there could be several people involved in the meeting, try to determine the number of people talking. Focus on accurately summarizing the main points and key details of the meeting. Do not comment on the style of the video (e.g., whether it is a voiceover or conversational). Provide a clear and informative summary that exclusively reference the video content.',
                # 'content': 'Why is the sky blue?',
                'content': transcript
            },
        ])
        return response
    except Exception as e:
        print('Error:', e.error)

def main(args):
    """
    Main function to transcribe and summarize a video.
    
    Parameters:
    args: Command-line arguments.
    """
    transcript_duration, summary_duration = 0, 0
    print("\nLeteScribe.")
    print("Transcribe. Summarize. Locally.")
    print("----------------------------------------------------------")

    if args.media_file: 
        if args.media_file.endswith('.mp4'):
            print(f">>> Media file path: {args.media_file}")
            video_path = args.media_file
        else:
            print("Only .mp4 files are supported. ")
            exit(1)
    else:
        print("Media file path missing. Please provide the path of the media file.")

    transcript_file_path = os.path.splitext(video_path)[0] + '_transcript.txt'
    if os.path.exists(transcript_file_path):
        print(f">>> Transcript file already exists at {transcript_file_path}.")
        transcript_confirm = input("Do you want to transcribe the video again? (y/n): ")
    else:
        transcript_confirm = 'y'
    
    if transcript_confirm.lower() == 'y':
        # Transcription:
        print(">>> Transcribing the video...")
        model = whisper.load_model(args.transcribe_only if args.transcribe_only else 'turbo')
        transcript_start_time = time.time()
        transcript = model.transcribe(video_path, verbose=True, language=args.language)
        transcript_end_time = time.time()
        transcript_duration = transcript_end_time - transcript_start_time
        transcript_formatted = save_transcript(transcript, transcript_file_path)
        print(f">>> Transcript saved to {transcript_file_path}")
    else:
        with open(transcript_file_path, 'r', encoding='utf-8') as file:
            transcript_formatted = file.read()
            print(f">>> Transcript loaded from {transcript_file_path}")
        transcript_duration = 0
    
    if args.transcribe_only:
        return
    else:
        if args.summarize_locally:
            print(">>> Summarizing the video locally...")
            summary_start_time = time.time()
            summary = ask_ollama(transcript_formatted, args.summarize_locally)
            summary_end_time = time.time()
            summary_duration = summary_end_time - summary_start_time
            print(f">>> Summary: \n {summary['message']['content']}")
            summary_file_path = f"{os.path.splitext(video_path)[0]}-{args.summarize_locally}-summary.txt"
            with open(summary_file_path, 'w', encoding='utf-8') as file:
                file.write(summary['message']['content'])
                print(f">>> Summary saved to {summary_file_path}")
        else: 
            print("Implementation on Google Gemini API is not available yet.")

    if transcript_duration > 0:
        print(f">>> Transcription took {transcript_duration:.2f} seconds.")
    else:
        print(f">>> Transcript skipped.")
    if summary_duration > 0:
        print(f">>> Summary took {summary_duration:.2f} seconds.")
    else:
        print(f">>> Summary skipped.")
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transcribe. Summarize. Locally.')
    parser.add_argument('-to', '--transcribe-only', nargs='?', type=str, const='turbo', help='Transcribe-only using the specified Whisper model (default model: turbo).')
    parser.add_argument('-l', '--language', type=str, default='en', help='Language of the video (default=en)')
    parser.add_argument('-m', '--media-file', type=str, default=None, help='Path of the video file (.mp4 only from now)')
    parser.add_argument('-sl', '--summarize-locally', nargs='?', type=str, const='llama3.1:8b', help='Summarise (locally) using the specified Ollama model (default=llama3.1:8b). If not specified, it will use the Google Gemini API.')
    args = parser.parse_args()
    main(args)