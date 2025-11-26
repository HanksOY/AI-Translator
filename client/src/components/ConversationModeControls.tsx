import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { Radio } from "lucide-react";

interface ConversationModeControlsProps {
  isActive: boolean;
  onToggle: () => void;
}

export default function ConversationModeControls({ isActive, onToggle }: ConversationModeControlsProps) {
  return (
    <div className="space-y-4">
      <div className="flex justify-center">
        <Button
          size="lg"
          variant={isActive ? "destructive" : "default"}
          onClick={onToggle}
          className="min-w-64"
          data-testid={isActive ? "button-end-conversation" : "button-start-conversation"}
        >
          {isActive ? "End Conversation" : "Start Conversation"}
        </Button>
      </div>
      
      {isActive && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          exit={{ opacity: 0, height: 0 }}
          className="flex flex-col items-center gap-2"
          data-testid="container-listening-indicator"
        >
          <div className="flex items-center gap-2 text-sm text-primary">
            <motion.div
              animate={{ scale: [1, 1.2, 1], opacity: [0.7, 1, 0.7] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            >
              <Radio className="w-4 h-4" />
            </motion.div>
            <span className="font-medium">Listening...</span>
          </div>
          
          <div className="flex gap-1 h-8 items-end" data-testid="container-vad-visualization">
            {[...Array(12)].map((_, i) => (
              <motion.div
                key={i}
                className="w-1 bg-primary rounded-full"
                animate={{
                  height: ["20%", "100%", "20%"],
                }}
                transition={{
                  duration: 0.8,
                  repeat: Infinity,
                  delay: i * 0.1,
                  ease: "easeInOut",
                }}
              />
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
