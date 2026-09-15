from faster_whisper import WhisperModel

from app.config import (
    WHISPER_MODEL,
    WHISPER_DEVICE,
    WHISPER_COMPUTE_TYPE
)


print(
    "========================================"
)

print(
    f"Loading Whisper model: {WHISPER_MODEL}"
)

print(
    "This may take some time the first time."
)

print(
    "========================================"
)


whisper_model = WhisperModel(
    WHISPER_MODEL,
    device=WHISPER_DEVICE,
    compute_type=WHISPER_COMPUTE_TYPE
)


print(
    "Whisper model loaded successfully."
)


def transcribe_audio(
    file_path: str
) -> str:

    segments, info = (
        whisper_model.transcribe(
            file_path,
            beam_size=5,
            vad_filter=True
        )
    )


    text_parts = []


    for segment in segments:

        text = segment.text.strip()


        if text:

            text_parts.append(
                text
            )


    result = " ".join(
        text_parts
    ).strip()


    print(
        f"Detected language: {info.language}"
    )


    print(
        f"Transcription: {result}"
    )


    return result