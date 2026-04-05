"use client";

import { useState } from "react";
import { Message } from "@/types";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { ChevronDown, ChevronUp, FileText, Loader2 } from "lucide-react";

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const [showSources, setShowSources] = useState(false);
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[75%] ${isUser ? "" : "w-full max-w-[75%]"}`}>
        <Card
          className={`border ${
            isUser
              ? "bg-primary text-primary-foreground border-primary"
              : "bg-card border-border"
          }`}
        >
          <CardContent className="p-3">
            {message.isLoading ? (
              <div className="flex items-center gap-2 text-muted-foreground">
                <Loader2 className="size-4 animate-spin" />
                <span className="text-sm">Thinking...</span>
              </div>
            ) : (
              <>
                <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
                  {message.content}
                </p>
                {!isUser && message.sources && message.sources.length > 0 && (
                  <Collapsible
                    open={showSources}
                    onOpenChange={setShowSources}
                    className="mt-3 border-t border-border pt-2"
                  >
                    <CollapsibleTrigger className="flex items-center gap-1 h-7 px-2 text-xs text-muted-foreground hover:text-foreground rounded transition-colors">
                        {showSources ? (
                          <ChevronUp className="size-3" />
                        ) : (
                          <ChevronDown className="size-3" />
                        )}
                        Sources ({message.sources.length})
                    </CollapsibleTrigger>
                    <CollapsibleContent className="mt-2 space-y-2">
                      {message.sources.map((source, idx) => (
                        <Card key={idx} className="bg-background border-border">
                          <CardContent className="p-2.5">
                            <div className="flex items-center justify-between mb-1.5">
                              <div className="flex items-center gap-1.5">
                                <FileText className="size-3 text-primary" />
                                <span className="text-xs font-semibold text-primary">
                                  {source.file}
                                </span>
                              </div>
                              <Badge
                                variant="secondary"
                                className="text-[0.65rem] px-1.5 py-0"
                              >
                                Page {source.page}
                              </Badge>
                            </div>
                            <p className="text-xs text-muted-foreground leading-snug line-clamp-3">
                              {source.excerpt}
                            </p>
                          </CardContent>
                        </Card>
                      ))}
                    </CollapsibleContent>
                  </Collapsible>
                )}
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
