// Basic types for the application

export interface UploadResponse {
  success: boolean;
  message: string;
  data?: Record<string, unknown>;
}

export interface AskQueryRequest {
  question: string;
  context?: string;
}

export interface AskQueryResponse {
  answer: string;
  confidence?: number;
  sources?: string[];
}

export interface CSVData {
  headers: string[];
  rows: string[][];
  totalRows: number;
}

export interface UploadFormData {
  file: File;
  description?: string;
} 