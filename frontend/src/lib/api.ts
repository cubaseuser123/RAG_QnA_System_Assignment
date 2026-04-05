import { AnswerResponse } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function askQuestion(question: string): Promise<AnswerResponse> {
  const response = await fetch(`${API_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    const error = await response
      .json()
      .catch(() => ({ detail: "API unreachable" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}
