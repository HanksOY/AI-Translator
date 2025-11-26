import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { Mic, StopCircle } from "lucide-react";

interface ConventionModeControlsProps {
  isRecording: boolean;
  onToggle: () => void;
}

export default function ConventionModeControls({ isRecording, onToggle }: ConventionModeControlsProps) {
  return (
    <div className="space-y-4">
      <div className="flex justify-center">
        <Button
          size="lg"
          variant={isRecording ? "destructive" : "default"}
          onClick={onToggle}
          className="min-w-64 gap-2"
          data-testid={isRecording ? "button-stop" : "button-speak"}
        >
          {isRecording ? (
            <>
              <StopCircle className="w-5 h-5" />
              Stop
            </>
          ) : (
            <>
              <Mic className="w-5 h-5" />
              Speak
            </>
          )}
        </Button>
      </div>
      
      {isRecording && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          exit={{ opacity: 0, height: 0 }}
          className="flex flex-col items-center gap-2"
          data-testid="container-recording-indicator"
        >
          <div className="flex items-center gap-2">
            <motion.div
              className="w-3 h-3 rounded-full bg-destructive"
              animate={{ scale: [1, 1.3, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
            />
            <span className="text-sm text-destructive font-medium">Recording...</span>
          </div>
        </motion.div>
      )}
    </div>
  );
}
