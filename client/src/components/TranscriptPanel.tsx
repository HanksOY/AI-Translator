import { ScrollArea } from "@/components/ui/scroll-area";
import TranscriptMessage from "./TranscriptMessage";
import { TranslationRecord } from "@shared/schema";

interface TranscriptPanelProps {
  records: TranslationRecord[];
}

export default function TranscriptPanel({ records }: TranscriptPanelProps) {
  return (
    <div className="flex-1 flex flex-col bg-background">
      <div className="border-b p-4">
        <h2 className="text-lg font-semibold" data-testid="text-panel-title">
          Translation History
        </h2>
        <p className="text-sm text-muted-foreground">
          {records.length} {records.length === 1 ? 'translation' : 'translations'}
        </p>
      </div>
      
      <ScrollArea className="flex-1 p-4">
        <div className="space-y-3" data-testid="container-transcript-list">
          {records.length === 0 ? (
            <div className="flex items-center justify-center h-40">
              <p className="text-muted-foreground text-sm" data-testid="text-empty-state">
                No translations yet. Start a conversation or type a message to begin.
              </p>
            </div>
          ) : (
            records.map((record) => (
              <TranscriptMessage
                key={record.id}
                sourceText={record.sourceText}
                translatedText={record.translatedText}
                sourceLanguage={record.sourceLanguage}
                targetLanguage={record.targetLanguage}
                timestamp={new Date(record.timestamp).toLocaleTimeString([], { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}
              />
            ))
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
