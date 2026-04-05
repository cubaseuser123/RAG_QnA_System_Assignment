export interface SourceNode {
  file: string;
  page: string;
  excerpt: string;
}

export interface AnswerResponse {
  answer: string;
  sources: SourceNode[];
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: SourceNode[];
  isLoading?: boolean;
}
