import React from 'react';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  isLoading?: boolean;
}

const bubbleBase =
  'px-4 py-2 rounded-lg max-w-[80%] whitespace-pre-line break-words shadow-sm';

export default function ChatMessage({ role, content, isLoading }: ChatMessageProps) {
  const isUser = role === 'user';
  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={
          bubbleBase +
          ' ' +
          (isUser
            ? 'bg-primary text-primary-foreground rounded-br-none'
            : 'bg-muted text-foreground rounded-bl-none border')
        }
      >
        {isLoading ? (
          <span className="italic text-muted-foreground">Thinking...</span>
        ) : (
          content
        )}
      </div>
    </div>
  );
} 