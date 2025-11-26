import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";
import ModeSelector, { Mode } from "./ModeSelector";
import ConversationModeControls from "./ConversationModeControls";
import ConventionModeControls from "./ConventionModeControls";
import TextInputArea from "./TextInputArea";

interface ControlAreaProps {
  mode: Mode;
  onModeChange: (mode: Mode) => void;
  isConversationActive: boolean;
  onConversationToggle: () => void;
  isRecording: boolean;
  onRecordingToggle: () => void;
  onSendMessage: (text: string) => void;
  onImageUpload: () => void;
  onClearHistory: () => void;
}

export default function ControlArea({
  mode,
  onModeChange,
  isConversationActive,
  onConversationToggle,
  isRecording,
  onRecordingToggle,
  onSendMessage,
  onImageUpload,
  onClearHistory,
}: ControlAreaProps) {
  return (
    <div className="border-t bg-card">
      <div className="max-w-4xl mx-auto p-4 space-y-4">
        <div className="flex items-center justify-between gap-4">
          <div className="flex-1">
            <ModeSelector mode={mode} onModeChange={onModeChange} />
          </div>
          <Button
            variant="outline"
            size="icon"
            onClick={onClearHistory}
            data-testid="button-clear-history"
          >
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>

        <Card className="p-4">
          {mode === "conversation" ? (
            <ConversationModeControls
              isActive={isConversationActive}
              onToggle={onConversationToggle}
            />
          ) : (
            <ConventionModeControls
              isRecording={isRecording}
              onToggle={onRecordingToggle}
            />
          )}
        </Card>

        <TextInputArea
          onSend={onSendMessage}
          onImageUpload={onImageUpload}
          disabled={isConversationActive || isRecording}
        />
      </div>
    </div>
  );
}
