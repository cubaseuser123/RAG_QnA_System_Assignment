"use client";

import { useState, useCallback } from "react";
import { Message } from "@/types";
import { askQuestion } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import ChatWindow from "@/components/ChatWindow";
import InputBar from "@/components/InputBar";

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = useCallback(async (question: string) => {
    const userMsg: Message = { id: crypto.randomUUID(), role: "user", content: question };
    const loadingMsg: Message = { id: crypto.randomUUID(), role: "assistant", content: "", isLoading: true };

    setMessages((prev) => [...prev, userMsg, loadingMsg]);
    setIsLoading(true);

    try {
      const response = await askQuestion(question);
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === loadingMsg.id
            ? { ...msg, content: response.answer, sources: response.sources, isLoading: false }
            : msg
        )
      );
    } catch (error) {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === loadingMsg.id
            ? {
                ...msg,
                content:
                  error instanceof Error
                    ? `Error: ${error.message}`
                    : "Something went wrong. Is the backend running?",
                isLoading: false,
              }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  return (
    <main className="flex flex-col h-screen max-w-3xl mx-auto w-full">
      <header className="flex items-center gap-3 px-5 py-4 border-b border-border">
        <h1 className="text-lg font-bold bg-gradient-to-r from-primary to-violet-400 bg-clip-text text-transparent">
          HelporaAI
        </h1>
        <Badge variant="secondary" className="text-[0.65rem]">
          RAG-powered Q&A
        </Badge>
      </header>
      <ChatWindow messages={messages} />
      <InputBar onSubmit={handleSubmit} isLoading={isLoading} />
    </main>
  );
}
