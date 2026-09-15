import {
  useRef,
  useState
} from "react";

import axios from "axios";


function VoiceRecorder({
  setQuestion,
  setAnswer,
  setSources,
  setAudioUrl
}) {

  const mediaRecorderRef =
    useRef(null);

  const audioChunksRef =
    useRef([]);


  const [recording, setRecording] =
    useState(false);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  /* ================================
     START RECORDING
  ================================= */

  const startRecording =
    async () => {

      setError("");


      try {

        if (
          !navigator.mediaDevices ||
          !navigator.mediaDevices.getUserMedia
        ) {

          setError(
            "Your browser does not support microphone recording."
          );

          return;
        }


        const stream =
          await navigator.mediaDevices
            .getUserMedia({
              audio: true
            });


        const mediaRecorder =
          new MediaRecorder(stream);


        mediaRecorderRef.current =
          mediaRecorder;


        audioChunksRef.current = [];


        mediaRecorder.ondataavailable =
          (event) => {

            if (
              event.data &&
              event.data.size > 0
            ) {

              audioChunksRef.current.push(
                event.data
              );

            }

          };


        mediaRecorder.onstop =
          async () => {

            const audioBlob =
              new Blob(
                audioChunksRef.current,
                {
                  type: "audio/webm"
                }
              );


            await sendAudio(
              audioBlob
            );


            stream
              .getTracks()
              .forEach(
                (track) =>
                  track.stop()
              );

          };


        mediaRecorder.start();

        setRecording(true);

      } catch (error) {

        console.error(
          "Microphone error:",
          error
        );


        setError(
          "Microphone permission is required."
        );

      }

    };


  /* ================================
     STOP RECORDING
  ================================= */

  const stopRecording = () => {

    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state !==
        "inactive"
    ) {

      mediaRecorderRef.current.stop();

      setRecording(false);

    }

  };


  /* ================================
     SEND AUDIO TO BACKEND
  ================================= */

  const sendAudio = async (
    audioBlob
  ) => {

    setLoading(true);

    setError("");


    setAnswer("");
    setSources([]);
    setAudioUrl("");


    try {

      const formData =
        new FormData();


      formData.append(
        "file",
        audioBlob,
        "question.webm"
      );


      const response =
        await axios.post(
          "/api/voice/ask",
          formData
        );


      const data =
        response.data;


      setQuestion(
        data.question || ""
      );


      setAnswer(
        data.answer || ""
      );


      setSources(
        data.sources || []
      );


      if (
        data.audio_url
      ) {

        const audioUrl =
          data.audio_url.startsWith(
            "http"
          )
            ? data.audio_url
            : `http://localhost:8000${data.audio_url}`;


        setAudioUrl(
          audioUrl
        );

      }

    } catch (error) {

      console.error(
        "Voice request error:",
        error
      );


      setError(
        error.response?.data?.detail ||
        "Something went wrong while processing your voice question."
      );

    } finally {

      setLoading(false);

    }

  };


  return (

    <div className="voice-recorder">


      {/* MICROPHONE */}

      <button
        type="button"
        className={
          recording
            ? "record-button recording"
            : "record-button"
        }
        onClick={
          recording
            ? stopRecording
            : startRecording
        }
        disabled={loading}
      >

        {loading
          ? "..."
          : recording
          ? "STOP"
          : "MIC"
        }

      </button>


      {/* STATUS */}

      <div className="record-status">

        {recording ? (

          <>
            <span className="live-dot"></span>
            Listening...
          </>

        ) : loading ? (

          <>
            <div className="loader"></div>

            Searching documents and
            generating answer...

          </>

        ) : (

          "Click the microphone and speak your question"

        )}

      </div>


      {/* FLOW */}

      <div className="voice-flow">

        <div className="flow-item">
          Speech
        </div>

        <div className="flow-arrow">
          →
        </div>

        <div className="flow-item">
          Retrieval
        </div>

        <div className="flow-arrow">
          →
        </div>

        <div className="flow-item">
          AI
        </div>

        <div className="flow-arrow">
          →
        </div>

        <div className="flow-item">
          Voice
        </div>

      </div>


      {/* ERROR */}

      {error && (

        <div className="voice-error">
          {error}
        </div>

      )}

    </div>

  );
}

export default VoiceRecorder;