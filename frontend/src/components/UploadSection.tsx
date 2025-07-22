import React from 'react';
import { UploadForm } from './UploadForm';
import ErrorAlert from './ErrorAlert';
import { CSVData } from '@/types';

interface UploadSectionProps {
  onFileUpload: (data: CSVData) => void;
  onError: (error: string) => void;
  error?: string | null;
}

export default function UploadSection({ onFileUpload, onError, error }: UploadSectionProps) {
  return (
    <div className="flex flex-col items-center w-full">
      <ErrorAlert message={error} />
      <UploadForm onFileUpload={onFileUpload} onError={onError} />
    </div>
  );
} 