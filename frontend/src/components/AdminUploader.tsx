"use client";
import { useState } from "react";
import { UploadCloud, CheckCircle, AlertCircle, Loader2 } from "lucide-react";

export default function AdminUploader() {
  const [text, setText] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");

  const handleUpload = async () => {
    if (!text) return;
    setStatus("loading");
    try {
      // Use env variable or default to localhost
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/api/upload`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      if (!res.ok) throw new Error("Failed");
      setStatus("success");
      setText("");
      setTimeout(() => setStatus("idle"), 3000);
    } catch (e) {
      setStatus("error");
    }
  };

  return (
    <div className="w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-xl shadow-xl p-6">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-white flex items-center gap-2">
          <UploadCloud className="text-blue-500" />
          Upload Context
        </h2>
        <p className="text-slate-400 text-sm mt-1">
          Paste text data here to train the database.
        </p>
      </div>

      <textarea
        className="w-full h-64 p-4 bg-slate-950 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-600 focus:ring-2 focus:ring-blue-600 focus:border-transparent outline-none resize-none font-mono text-sm"
        placeholder="Paste your documents, policies, or menu items here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <div className="mt-4 flex justify-end">
        <button
          onClick={handleUpload}
          disabled={status === "loading" || !text}
          className={`px-6 py-2.5 rounded-lg font-medium text-sm flex items-center gap-2 transition-colors ${
            status === "success" 
              ? "bg-green-600 text-white"
              : status === "error"
              ? "bg-red-600 text-white"
              : "bg-blue-600 hover:bg-blue-700 text-white"
          }`}
        >
          {status === "loading" && <Loader2 className="animate-spin" size={18} />}
          {status === "success" && <CheckCircle size={18} />}
          {status === "error" && <AlertCircle size={18} />}
          
          {status === "loading" ? "Processing..." : 
           status === "success" ? "Indexed!" : 
           status === "error" ? "Failed" : "Upload to DB"}
        </button>
      </div>
    </div>
  );
}