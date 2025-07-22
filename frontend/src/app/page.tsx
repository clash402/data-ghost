'use client';

import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { UploadForm } from '@/components/UploadForm';
import { AnswerCard } from '@/components/AnswerCard';
import { CSVData, AskQueryResponse } from '@/types';
import { useAskQuery } from '@/hooks/useAskQuery';
import Logo from '@/components/Logo';
import Footer from '@/components/Footer';
import ChatMessage from '@/components/ChatMessage';
import { countTokens } from '@/lib/csv-parser';

// Create a client
const queryClient = new QueryClient();

function DataGhostApp() {
  const [csvData, setCsvData] = useState<CSVData | null>(null);
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([]);
  const [error, setError] = useState<string | null>(null);

  const askQueryMutation = useAskQuery();

  const handleFileUpload = (data: CSVData) => {
    setCsvData(data);
    setError(null);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
  };

  const handleAskQuestion = async () => {
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    if (!csvData) {
      setError('Please upload a CSV file first');
      return;
    }

    // Add user message
    setChatHistory((prev) => [...prev, { role: 'user', content: question.trim() }]);
    setQuestion('');
    try {
      const response = await askQueryMutation.mutateAsync({
        question: question.trim(),
        context: JSON.stringify(csvData),
      });
      setChatHistory((prev) => [...prev, { role: 'assistant', content: response.answer }]);
      setError(null);
    } catch (err) {
      // Always handle errors gracefully, never throw
      setChatHistory((prev) => [
        ...prev,
        { role: 'assistant', content: `Sorry, I couldn't get an answer from the server. This might be because the backend service is offline, your internet connection is unstable, or there was a temporary issue.\n\nPlease check your connection and try again. If the problem persists, make sure the backend server is running and reachable.` },
      ]);
      setError(null); // Clear any previous error to avoid overlays
      // Optionally log error for debugging
      // console.error('Chat error:', err);
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Top Header */}
      <header className="w-full flex items-center px-4 py-4">
        <Logo />
      </header>
      <main className="flex-1 flex flex-col items-center gap-24">
        <div className="w-full max-w-3xl flex-1 flex flex-col px-4 mt-8" style={{ maxHeight: 'calc(100vh - 2 * 5rem - 2 * 2rem)' }}>
          {!csvData ? (
            <div className="flex flex-1 items-center justify-center">
              <UploadForm onFileUpload={handleFileUpload} onError={handleError} />
            </div>
          ) : (
            <div className="flex flex-col h-full max-h-[80vh] border rounded-lg bg-card overflow-hidden">
              <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-background">
                {chatHistory.length === 0 && (
                  <div className="text-center text-muted-foreground text-sm py-8">
                    Ask a question about your uploaded CSV to get started!
                  </div>
                )}
                {chatHistory.map((msg, idx) => (
                  <ChatMessage key={idx} role={msg.role} content={msg.content} />
                ))}
                {askQueryMutation.isPending && (
                  <ChatMessage role="assistant" content="Thinking..." isLoading />
                )}
              </div>
              <form
                className="flex flex-col gap-1 border-t bg-background px-4 py-3"
                onSubmit={e => { e.preventDefault(); handleAskQuestion(); }}
              >
                <div className="flex items-center gap-2">
                  <input
                    type="text"
                    placeholder="Type your question about the data..."
                    value={question}
                    onChange={e => setQuestion(e.target.value)}
                    className="flex-1 px-4 py-2 border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground"
                    disabled={askQueryMutation.isPending}
                  />
                  <button
                    type="submit"
                    disabled={askQueryMutation.isPending || !question.trim()}
                    className="px-6 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {askQueryMutation.isPending ? 'Sending...' : 'Send'}
                  </button>
                </div>
                <div className="text-xs text-muted-foreground mt-1 px-1">
                  Prompt tokens: {countTokens(question)} &bull; Completion tokens: 0 &bull; Estimated cost $0.0000
                </div>
              </form>
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default function Home() {
  return (
    <QueryClientProvider client={queryClient}>
      <DataGhostApp />
    </QueryClientProvider>
  );
}
