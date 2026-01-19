import AdminUploader from "@/components/AdminUploader";
import RagChatWidget from "@/components/RagChatWidget";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-10 bg-slate-950">
      
      <div className="text-center mb-10 space-y-2">
        <h1 className="text-4xl font-bold text-white tracking-tight">
          Enterprise RAG System
        </h1>
        <p className="text-slate-400 text-lg">
          Secure Knowledge Base & Database Chat
        </p>
      </div>

      {/* Main Content */}
      <AdminUploader />

      {/* Chat Widget */}
      <RagChatWidget />
    </main>
  );
}