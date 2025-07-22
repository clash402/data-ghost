import React from 'react';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  isLoading?: boolean;
}

const bubbleBase =
  'px-4 py-2 rounded-lg max-w-[80%] whitespace-pre-line break-words shadow-sm backdrop-blur-sm';

export default function ChatMessage({ role, content, isLoading }: ChatMessageProps) {
  const isUser = role === 'user';
  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={
          bubbleBase +
          ' ' +
          (isUser
            ? 'bg-white/40 dark:bg-slate-700/40 text-slate-800 dark:text-slate-100 rounded-br-none border border-white/50 dark:border-slate-600/50'
            : 'bg-white/30 dark:bg-slate-800/30 text-slate-800 dark:text-slate-100 rounded-bl-none border border-white/40 dark:border-slate-700/40')
        }
      >
        {isLoading ? (
          <span className="italic text-slate-500 dark:text-slate-400">Thinking...</span>
        ) : (
          content
        )}
      </div>
    </div>
  );
} 