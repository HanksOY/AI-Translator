import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Send, ImagePlus } from "lucide-react";

interface TextInputAreaProps {
  onSend: (text: string) => void;
  onImageUpload?: () => void;
  disabled?: boolean;
}

export default function TextInputArea({ onSend, onImageUpload, disabled = false }: TextInputAreaProps) {
  const [text, setText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      onSend(text);
      setText("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 w-full">
      <Button
        type="button"
        variant="outline"
        size="icon"
        onClick={onImageUpload}
        disabled={disabled}
        data-testid="button-image-upload"
      >
        <ImagePlus className="w-4 h-4" />
      </Button>
      
      <Input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type a message to translate..."
        disabled={disabled}
        className="flex-1"
        data-testid="input-message"
      />
      
      <Button
        type="submit"
        size="icon"
        disabled={disabled || !text.trim()}
        data-testid="button-send"
      >
        <Send className="w-4 h-4" />
      </Button>
    </form>
  );
}
