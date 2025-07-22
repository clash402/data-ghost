import React from 'react';

interface ErrorAlertProps {
  message?: string | null;
}

export default function ErrorAlert({ message }: ErrorAlertProps) {
  if (!message) return null;
  return (
    <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4 mb-2">
      <p className="text-destructive text-sm">{message}</p>
    </div>
  );
} 