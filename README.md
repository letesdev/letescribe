# _LeteScribe_
Transcribe. Summarize. Locally.

## Overview
_LeteScribe_ is a simple Python-based application that transcribes and summarizes automatically your videos, **locally**. 

It uses [Whisper](https://github.com/openai/whisper) for automatic video transcription and [Ollama](https://github.com/ollama/ollama) for summarizing it. 

## Requirements

To run _LeteScribe_, you will need:

- Python 3.8+
- [Whisper package and model](https://github.com/openai/whisper?tab=readme-ov-file#setup): `pip install -U openai-whisper`
- Ollama: download on your computer and download a model from the [model library](https://github.com/ollama/ollama?tab=readme-ov-file#model-library). 


## Usage

To use _LeteScribe_, simply run the 
`letescribe.py` script with the following command:

```
python src/letescribe.py --language es --media-file <video_file_path>  --summarize-locally
```

Replace `<video_file_path>` with the path to your video file. The options available are:

- `--transcribe-only`: Transcribes the video only, skipping summary generation.
- `--language`: Specify the language of the video (default: English).
- `--media-file`: Path to the video file. It is required, if forgotten, it will ask you for the video path. 
- `--summarize-locally`: Summarizes using Ollama API (locally).


## Troubleshooting
For any issues or errors encountered while using LeTescribe, please refer to the following:

- Check if your video file is in `.mp4` format. I believe Whisper accepts more formats, including audio formats, but `.mp4` was enough for my usage. 
- Verify that you have the correct Whisper model loaded (`turbo` by default).
- Ensure that Ollama is running and you have the correct model loaded (`llama3.1:8b` by default)
- Write an issue on this repo. 