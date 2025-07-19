import Papa from 'papaparse';
import { CSVData } from '@/types';

export const parseCSV = (file: File): Promise<CSVData> => {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        if (results.errors.length > 0) {
          reject(new Error(`CSV parsing errors: ${results.errors.map(e => e.message).join(', ')}`));
          return;
        }

        const headers = results.meta.fields || [];
        const rows = results.data as string[][];
        
        resolve({
          headers,
          rows,
          totalRows: rows.length,
        });
      },
      error: (error) => {
        reject(new Error(`CSV parsing failed: ${error.message}`));
      },
    });
  });
};

export const countTokens = (text: string): number => {
  // Simple token counting - roughly 4 characters per token
  // This is a basic implementation and can be improved
  return Math.ceil(text.length / 4);
}; 