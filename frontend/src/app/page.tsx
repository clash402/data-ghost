'use client';

import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { UploadForm } from '@/components/UploadForm';
import { AnswerCard } from '@/components/AnswerCard';
import { CSVData, AskQueryResponse } from '@/types';
import { useAskQuery } from '@/hooks/useAskQuery';

// Create a client
const queryClient = new QueryClient();

function DataGhostApp() {
  const [csvData, setCsvData] = useState<CSVData | null>(null);
  const [question, setQuestion] = useState('');
  const [currentAnswer, setCurrentAnswer] = useState<AskQueryResponse | null>(null);
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

    try {
      const response = await askQueryMutation.mutateAsync({
        question: question.trim(),
        context: JSON.stringify(csvData),
      });
      setCurrentAnswer(response);
      setError(null);
    } catch (err) {
      setError('Failed to get answer. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Header */}
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-bold tracking-tight">
              Data Ghost
            </h1>
            <p className="text-xl text-muted-foreground">
              Upload your CSV data and ask questions about it!
            </p>
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4">
              <p className="text-destructive text-sm">{error}</p>
            </div>
          )}

          {/* Upload Section */}
          <div className="flex justify-center">
            <UploadForm onFileUpload={handleFileUpload} onError={handleError} />
          </div>

          {/* Data Summary */}
          {csvData && (
            <div className="bg-card border rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Data Summary</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="font-medium">Columns:</span> {csvData.headers.length}
                </div>
                <div>
                  <span className="font-medium">Rows:</span> {csvData.totalRows}
                </div>
                <div>
                  <span className="font-medium">File Size:</span> {csvData.headers.join(', ')}
                </div>
              </div>
            </div>
          )}

          {/* Query Section */}
          {csvData && (
            <div className="space-y-4">
              <div className="flex gap-4">
                <input
                  type="text"
                  placeholder="Ask a question about your data..."
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  className="flex-1 px-4 py-2 border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground"
                  onKeyPress={(e) => e.key === 'Enter' && handleAskQuestion()}
                />
                <button
                  onClick={handleAskQuestion}
                  disabled={askQueryMutation.isPending || !question.trim()}
                  className="px-6 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {askQueryMutation.isPending ? 'Asking...' : 'Ask'}
                </button>
              </div>

              {/* Answer Display */}
              {currentAnswer && (
                <AnswerCard
                  question={question}
                  answer={currentAnswer}
                  isLoading={askQueryMutation.isPending}
                />
              )}
            </div>
          )}
        </div>
      </div>
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
