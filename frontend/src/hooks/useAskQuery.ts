import { useMutation } from '@tanstack/react-query';
import { apiClient } from '@/api/client';
import { AskQueryRequest, AskQueryResponse } from '@/types';

export const useAskQuery = () => {
  return useMutation<AskQueryResponse, Error, AskQueryRequest>({
    mutationFn: (request: AskQueryRequest) => apiClient.askQuery(request),
    onError: (error) => {
      console.error('Ask query failed:', error);
    },
  });
}; 