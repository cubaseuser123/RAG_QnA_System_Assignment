"use client";

import { useState, FormEvent } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { SendHorizonal, Loader2 } from "lucide-react";

interface InputBarProps {
  onSubmit: (question: string) => void;
  isLoading: boolean;
}

export default function InputBar({ onSubmit, isLoading }: InputBarProps) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;
    onSubmit(trimmed);
    setInput("");
  };

  return (
    <form
      className="flex items-center gap-2 border-t border-border bg-card p-4"
      onSubmit={handleSubmit}
    >
      <Input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask a question about your documents..."
        disabled={isLoading}
        autoFocus
        className="flex-1 bg-background"
      />
      <Button type="submit" disabled={isLoading || !input.trim()} size="default">
        {isLoading ? (
          <Loader2 className="size-4 animate-spin" />
        ) : (
          <SendHorizonal className="size-4" />
        )}
      </Button>
    </form>
  );
}
