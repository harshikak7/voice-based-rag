import pyttsx3


def generate_speech(
    text: str,
    output_path: str
):

    engine = pyttsx3.init()


    # Speech speed
    engine.setProperty(
        "rate",
        170
    )


    # Volume
    engine.setProperty(
        "volume",
        1.0
    )


    engine.save_to_file(
        text,
        output_path
    )


    engine.runAndWait()


    engine.stop()


    return output_path