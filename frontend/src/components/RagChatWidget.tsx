"use client";
import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { Send, MessageSquare, X, Loader2, Sparkles } from "lucide-react";

export default function RagChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([{ role: "model", text: "Ready to search your database." }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isOpen]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = input;
    setMessages((prev) => [...prev, { role: "user", text: userMsg }]);
    setInput("");
    setLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMsg }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: "model", text: data.answer }]);
    } catch (error) {
      setMessages((prev) => [...prev, { role: "model", text: "Error connecting to DB." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ zIndex: 9999 }}>
      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 p-4 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 transition-all"
      >
        {isOpen ? <X size={24} /> : <MessageSquare size={24} />}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-96 h-[550px] bg-slate-900 border border-slate-700 rounded-xl shadow-2xl flex flex-col overflow-hidden">
          
          {/* Header */}
          <div className="bg-slate-800 p-4 border-b border-slate-700 flex items-center gap-2">
            <Sparkles className="text-blue-400" size={18} />
            <span className="font-semibold text-white">RAG Assistant</span>
            <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full ml-auto">Online</span>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-900">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[85%] p-3 rounded-lg text-sm ${
                  m.role === "user" 
                    ? "bg-blue-600 text-white" 
                    : "bg-slate-800 border border-slate-700 text-slate-200"
                }`}>
                  <ReactMarkdown>{m.text}</ReactMarkdown>
                </div>
              </div>
            ))}
            {loading && <Loader2 className="animate-spin text-slate-500 ml-2" size={18} />}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 bg-slate-900 border-t border-slate-800 flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Ask a question..."
              className="flex-1 bg-slate-950 border border-slate-700 text-white rounded-full px-4 py-2 focus:outline-none focus:border-blue-500 text-sm"
            />
            <button 
              onClick={handleSend} 
              disabled={loading} 
              className="text-white bg-blue-600 p-2 rounded-full hover:bg-blue-700 disabled:opacity-50"
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}