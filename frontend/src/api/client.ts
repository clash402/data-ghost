import { AskQueryRequest, AskQueryResponse, UploadResponse } from '@/types';

// Ensure we always use HTTPS for the deployed backend
const getApiBaseUrl = () => {
  const envUrl = process.env.NEXT_PUBLIC_API_URL;
  if (envUrl) {
    // If it's the deployed backend URL, ensure it uses HTTPS
    if (envUrl.includes('data-ghost-backend.fly.dev')) {
      return envUrl.replace('http://', 'https://');
    }
    return envUrl;
  }
  return 'https://data-ghost-backend.fly.dev';
};

const API_BASE_URL = getApiBaseUrl();
console.log('🔧 API_BASE_URL from client.ts:', API_BASE_URL);

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    return response.json();
  }

  async uploadFile(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return response.json();
  }

  async askQuery(request: AskQueryRequest): Promise<AskQueryResponse> {
    return this.request<AskQueryResponse>('/ask', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async healthCheck(): Promise<{ status: string; service: string; version: string; environment: string }> {
    return this.request<{ status: string; service: string; version: string; environment: string }>('/health/');
  }
}

export const apiClient = new ApiClient(); 