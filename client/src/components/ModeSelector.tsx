import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

export type Mode = "conversation" | "convention";

interface ModeSelectorProps {
  mode: Mode;
  onModeChange: (mode: Mode) => void;
}

export default function ModeSelector({ mode, onModeChange }: ModeSelectorProps) {
  return (
    <Tabs value={mode} onValueChange={(value) => onModeChange(value as Mode)} className="w-full">
      <TabsList className="grid w-full grid-cols-2" data-testid="tabs-mode-selector">
        <TabsTrigger value="conversation" data-testid="tab-conversation">
          Conversation Mode (Hands-off)
        </TabsTrigger>
        <TabsTrigger value="convention" data-testid="tab-convention">
          Convention Mode (Hands-on)
        </TabsTrigger>
      </TabsList>
    </Tabs>
  );
}
