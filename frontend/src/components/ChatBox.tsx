import React from 'react';
import ChatMessage from './ChatMessage';
import { countTokens } from '@/lib/csv-parser';

interface ChatBoxProps {
  chatHistory: Array<{ role: 'user' | 'assistant'; content: string }>;
  question: string;
  setQuestion: (q: string) => void;
  onSend: () => void;
  isLoading: boolean;
}

export default function ChatBox({ chatHistory, question, setQuestion, onSend, isLoading }: ChatBoxProps) {
  return (
    <div className="flex flex-col h-full max-h-[70vh] sm:max-h-[75vh] lg:max-h-[80vh] border rounded-xl glass-card overflow-hidden transition-all duration-300">
      <div className="flex-1 overflow-y-auto p-3 sm:p-4 lg:p-6 space-y-3 sm:space-y-4 bg-transparent">
        {chatHistory.length === 0 && (
          <div className="text-center text-slate-600 dark:text-slate-400 text-sm sm:text-base py-6 sm:py-8 transition-colors duration-300">
            Ask a question about your uploaded CSV to get started!
          </div>
        )}
        {chatHistory.map((msg, idx) => (
          <ChatMessage key={idx} role={msg.role} content={msg.content} />
        ))}
        {isLoading && (
          <ChatMessage role="assistant" content="Thinking..." isLoading />
        )}
      </div>
      <form
        className="flex flex-col gap-1 sm:gap-2 border-t bg-transparent px-3 sm:px-4 lg:px-6 py-3 sm:py-4"
        onSubmit={e => { e.preventDefault(); onSend(); }}
      >
        <div className="flex items-center gap-2 sm:gap-3">
          <input
            type="text"
            placeholder="Type your question about the data..."
            value={question}
            onChange={e => setQuestion(e.target.value)}
            className="ghost-input flex-1 text-sm sm:text-base"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !question.trim()}
            className="ghost-btn text-sm sm:text-base px-3 sm:px-4 py-2"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
        <div className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1 px-1 transition-colors duration-300">
          Prompt tokens: {countTokens(question)} &bull; Completion tokens: 0 &bull; Estimated cost $0.0000
        </div>
      </form>
    </div>
  );
} 