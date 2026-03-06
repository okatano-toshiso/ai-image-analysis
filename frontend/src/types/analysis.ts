export interface AnalysisLog {
  id: number;
  image_path: string | null;
  is_success: boolean;
  message: string | null;
  class_label: number | null;
  confidence: number | null;
  request_timestamp: string | null;
  response_timestamp: string | null;
}

export interface AnalyzeResult {
  log: AnalysisLog;
  api_response: {
    is_success: boolean;
    message: string;
    estimated_data: {
      class_label?: number;
      confidence?: number;
    };
  };
}
