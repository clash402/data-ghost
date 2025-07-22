'use client';

import { useState } from 'react';
import { Upload, FileText } from 'lucide-react';
import { parseCSV } from '@/lib/csv-parser';
import { CSVData } from '@/types';
import ErrorAlert from './ErrorAlert';

interface UploadFormProps {
  onFileUpload: (data: CSVData) => void;
  onError: (error: string) => void;
  error?: string | null;
}

export const UploadForm = ({ onFileUpload, onError, error }: UploadFormProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'text/csv') {
      setSelectedFile(file);
    } else {
      onError('Please select a valid CSV file');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      onError('Please select a file first');
      return;
    }

    setIsLoading(true);
    try {
      const csvData = await parseCSV(selectedFile);
      onFileUpload(csvData);
    } catch (error) {
      onError(error instanceof Error ? error.message : 'Failed to parse CSV file');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center w-full max-w-sm sm:max-w-lg lg:max-w-lg mx-auto glass-card px-3 sm:px-4 py-4 sm:py-6 rounded-xl transition-all duration-300">
      <ErrorAlert message={error} />
      <div className="w-full max-w-sm sm:max-w-md lg:max-w-lg text-center">
        <div className="mb-4 sm:mb-6">
          <h2 className="text-lg sm:text-xl lg:text-2xl font-semibold text-slate-800 dark:text-slate-100 flex items-center justify-center gap-2 mb-2 transition-colors duration-300">
            <FileText className="h-4 w-4 sm:h-5 sm:w-5 lg:h-6 lg:w-6" />
            Upload CSV File
          </h2>
          <p className="text-xs sm:text-sm lg:text-base text-slate-600 dark:text-slate-400 transition-colors duration-300">
            Select a CSV file to analyze and query
          </p>
        </div>
        <div className="space-y-3 sm:space-y-4">
          <div className="space-y-2">
            <label htmlFor="file-upload" className="text-xs sm:text-sm lg:text-base font-medium text-slate-700 dark:text-slate-300 transition-colors duration-300">
              CSV File
            </label>
            <input
              id="file-upload"
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              disabled={isLoading}
              className="ghost-input w-full text-xs py-4 sm:text-sm lg:text-base"
            />
          </div>
          <button
            onClick={handleUpload}
            disabled={!selectedFile || isLoading}
            className="ghost-btn w-full text-xs sm:text-sm lg:text-base flex py-4 items-center justify-center"
          >
            {isLoading ? (
              'Processing...'
            ) : (
              <>
                <Upload className="mr-2 h-4 w-4 sm:h-4 sm:w-4 lg:h-5 lg:w-5" />
                Upload & Parse
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}; 