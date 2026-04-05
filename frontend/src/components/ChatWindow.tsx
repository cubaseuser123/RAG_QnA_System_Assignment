"use client";

import { useRef, useEffect } from "react";
import { Message } from "@/types";
import { ScrollArea } from "@/components/ui/scroll-area";
import MessageBubble from "./MessageBubble";
import { MessageSquare } from "lucide-react";

interface ChatWindowProps {
  messages: Message[];
}

export default function ChatWindow({ messages }: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <ScrollArea className="flex-1">
      <div className="flex flex-col gap-4 p-5">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center text-center py-24 text-muted-foreground">
            <MessageSquare className="size-12 mb-4 opacity-30" />
            <h2 className="text-xl font-semibold text-foreground mb-2">
              HelporaAI RAG Assistant
            </h2>
            <p className="text-sm">Ask questions about your ingested documents.</p>
            <p className="text-xs text-primary/60 mt-4">
              Try: &quot;What is the transformer architecture?&quot;
            </p>
          </div>
        ) : (
          messages.map((msg) => <MessageBubble key={msg.id} message={msg} />)
        )}
        <div ref={bottomRef} />
      </div>
    </ScrollArea>
  );
}
