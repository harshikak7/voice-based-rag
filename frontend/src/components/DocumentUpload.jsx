import { useRef, useState } from "react";
import axios from "axios";

function DocumentUpload() {

  const fileInputRef = useRef(null);

  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);

  const [message, setMessage] = useState("");

  const [success, setSuccess] = useState(false);


  /* ================================
     FILE SELECT
  ================================= */

  const handleFileChange = (event) => {

    const selectedFile =
      event.target.files?.[0];

    setMessage("");
    setSuccess(false);

    if (!selectedFile) {
      setFile(null);
      return;
    }

    if (
      !selectedFile.name
        .toLowerCase()
        .endsWith(".pdf")
    ) {

      setFile(null);

      setMessage(
        "Please select a PDF file."
      );

      return;
    }

    setFile(selectedFile);
  };


  /* ================================
     UPLOAD
  ================================= */

  const uploadFile = async () => {

    if (!file) {

      setMessage(
        "Please select a PDF first."
      );

      setSuccess(false);

      return;
    }

    setLoading(true);

    setMessage(
      "Uploading and indexing your PDF..."
    );

    setSuccess(false);


    try {

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );


      const response =
        await axios.post(
          "/api/documents/upload",
          formData
        );


      const data =
        response.data?.data;


      if (data) {

        setMessage(
          `${data.filename} indexed successfully. ${data.chunks} chunks created.`
        );

      } else {

        setMessage(
          "Document uploaded successfully."
        );

      }


      setSuccess(true);

      setFile(null);


      if (fileInputRef.current) {

        fileInputRef.current.value = "";

      }


    } catch (error) {

      console.error(
        "Upload error:",
        error
      );


      const detail =
        error.response?.data?.detail;


      setMessage(
        detail ||
        "Failed to upload document. Make sure the backend is running."
      );


      setSuccess(false);


    } finally {

      setLoading(false);

    }
  };


  return (

    <div className="upload-container">


      {/* UPLOAD AREA */}

      <label
        htmlFor="pdf-upload"
        className="upload-box"
      >

        <div className="upload-icon">
          PDF
        </div>


        <div className="upload-main-text">

          {file
            ? file.name
            : "Choose a PDF document"
          }

        </div>


        <div className="upload-sub-text">

          {file
            ? `${(
                file.size /
                1024 /
                1024
              ).toFixed(2)} MB`
            : "Click here to browse"
          }

        </div>


        <input
          ref={fileInputRef}
          id="pdf-upload"
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileChange}
          hidden
        />

      </label>


      {/* BUTTON */}

      <div className="upload-action">

        <button
          type="button"
          className="upload-button"
          onClick={uploadFile}
          disabled={
            loading ||
            !file
          }
        >

          {loading
            ? "Processing..."
            : "Upload & Index"
          }

        </button>

      </div>


      {/* MESSAGE */}

      {message && (

        <div
          className={
            success
              ? "status-message success"
              : "status-message error"
          }
        >

          {message}

        </div>

      )}

    </div>

  );
}

export default DocumentUpload;