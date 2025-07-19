'use client';

import { MessageSquare, Copy, Check } from 'lucide-react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { AskQueryResponse } from '@/types';

interface AnswerCardProps {
  question: string;
  answer: AskQueryResponse;
  isLoading?: boolean;
}

export const AnswerCard = ({ question, answer, isLoading = false }: AnswerCardProps) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(answer.answer);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy text:', error);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MessageSquare className="h-5 w-5" />
          Query Response
        </CardTitle>
        <CardDescription className="text-sm text-muted-foreground">
          {question}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        ) : (
          <>
            <div className="prose prose-sm max-w-none">
              <p className="text-sm leading-relaxed">{answer.answer}</p>
            </div>
            
            {answer.confidence && (
              <div className="text-xs text-muted-foreground">
                Confidence: {Math.round(answer.confidence * 100)}%
              </div>
            )}
            
            {answer.sources && answer.sources.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-sm font-medium">Sources:</h4>
                <ul className="text-xs text-muted-foreground space-y-1">
                  {answer.sources.map((source, index) => (
                    <li key={index}>{source}</li>
                  ))}
                </ul>
              </div>
            )}
            
            <div className="flex justify-end">
              <Button
                variant="outline"
                size="sm"
                onClick={handleCopy}
                className="flex items-center gap-2"
              >
                {copied ? (
                  <>
                    <Check className="h-4 w-4" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="h-4 w-4" />
                    Copy Answer
                  </>
                )}
              </Button>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}; 