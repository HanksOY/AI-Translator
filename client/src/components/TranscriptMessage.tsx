import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface TranscriptMessageProps {
  sourceText: string;
  translatedText: string;
  sourceLanguage: string;
  targetLanguage: string;
  timestamp: string;
}

export default function TranscriptMessage({
  sourceText,
  translatedText,
  sourceLanguage,
  targetLanguage,
  timestamp,
}: TranscriptMessageProps) {
  return (
    <Card className="p-4 space-y-3" data-testid="card-transcript-message">
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 space-y-1">
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="text-xs" data-testid="badge-source-lang">
              {sourceLanguage}
            </Badge>
            <p className="text-sm text-foreground" data-testid="text-source">
              {sourceText}
            </p>
          </div>
        </div>
      </div>
      
      <div className="flex items-start gap-2 pl-4 border-l-2 border-primary/30">
        <Badge variant="secondary" className="text-xs" data-testid="badge-target-lang">
          {targetLanguage}
        </Badge>
        <p className="text-sm text-muted-foreground flex-1" data-testid="text-translated">
          {translatedText}
        </p>
      </div>
      
      <div className="flex justify-end">
        <span className="text-xs text-muted-foreground" data-testid="text-timestamp">
          {timestamp}
        </span>
      </div>
    </Card>
  );
}
