'use client';

import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { CSVData } from '@/types';
import { useAskQuery } from '@/hooks/useAskQuery';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ChatBox from '@/components/ChatBox';
import { UploadForm } from '@/components/UploadForm';

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
    <div className="min-h-screen bg-background flex flex-col transition-colors duration-500">
      <Header />
      <main className="flex-1 flex flex-col items-center gap-16 sm:gap-20 lg:gap-24">
        <div className="w-full max-w-2xl sm:max-w-3xl lg:max-w-4xl flex-1 flex flex-col px-4 sm:px-6 lg:px-8 mt-6 sm:mt-8" style={{ maxHeight: 'calc(100vh - 2 * 5rem - 2 * 2rem)' }}>
          {!csvData ? (
            <UploadForm onFileUpload={handleFileUpload} onError={handleError} error={error} />
          ) : (
            <ChatBox
              chatHistory={chatHistory}
              question={question}
              setQuestion={setQuestion}
              onSend={handleAskQuestion}
              isLoading={askQueryMutation.isPending}
            />
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
