'use client';

import { useState } from 'react';
import { Upload, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { parseCSV } from '@/lib/csv-parser';
import { CSVData } from '@/types';

interface UploadFormProps {
  onFileUpload: (data: CSVData) => void;
  onError: (error: string) => void;
}

export const UploadForm = ({ onFileUpload, onError }: UploadFormProps) => {
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
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="h-5 w-5" />
          Upload CSV File
        </CardTitle>
        <CardDescription>
          Select a CSV file to analyze and query
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="file-upload">CSV File</Label>
          <Input
            id="file-upload"
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={isLoading}
          />
        </div>
        <Button
          onClick={handleUpload}
          disabled={!selectedFile || isLoading}
          className="w-full"
        >
          {isLoading ? (
            'Processing...'
          ) : (
            <>
              <Upload className="mr-2 h-4 w-4" />
              Upload & Parse
            </>
          )}
        </Button>
      </CardContent>
    </Card>
  );
}; 