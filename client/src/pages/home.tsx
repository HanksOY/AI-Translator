import { useState } from "react";
import AvatarPanel from "@/components/AvatarPanel";
import TranscriptPanel from "@/components/TranscriptPanel";
import ControlArea from "@/components/ControlArea";
import { Mode } from "@/components/ModeSelector";
import { TranslationRecord } from "@shared/schema";
import { useToast } from "@/hooks/use-toast";

export default function Home() {
  const [mode, setMode] = useState<Mode>("conversation");
  const [isConversationActive, setIsConversationActive] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const { toast } = useToast();
  
  // TODO: remove mock functionality - Replace with real translation records from API
  const [records, setRecords] = useState<TranslationRecord[]>([
    {
      id: '1',
      sourceText: 'Welcome to the Real-time AI Translation Platform.',
      translatedText: 'Bienvenue sur la plateforme de traduction IA en temps réel.',
      sourceLanguage: 'EN',
      targetLanguage: 'FR',
      timestamp: new Date(Date.now() - 600000),
    },
    {
      id: '2',
      sourceText: 'This platform provides professional translation for Finance and Healthcare.',
      translatedText: 'Cette plateforme fournit une traduction professionnelle pour la Finance et la Santé.',
      sourceLanguage: 'EN',
      targetLanguage: 'FR',
      timestamp: new Date(Date.now() - 300000),
    },
  ]);

  const handleConversationToggle = () => {
    setIsConversationActive(!isConversationActive);
    toast({
      title: !isConversationActive ? "Conversation Started" : "Conversation Ended",
      description: !isConversationActive 
        ? "The AI is now listening continuously..." 
        : "Conversation mode has been stopped.",
    });
  };

  const handleRecordingToggle = () => {
    setIsRecording(!isRecording);
    toast({
      title: !isRecording ? "Recording Started" : "Recording Stopped",
      description: !isRecording 
        ? "Press Stop when you're done speaking." 
        : "Processing your speech...",
    });
  };

  const handleSendMessage = (text: string) => {
    // TODO: remove mock functionality - Send to real translation API
    const newRecord: TranslationRecord = {
      id: Date.now().toString(),
      sourceText: text,
      translatedText: `[Translated] ${text}`,
      sourceLanguage: 'EN',
      targetLanguage: 'FR',
      timestamp: new Date(),
    };
    
    setRecords([...records, newRecord]);
    
    toast({
      title: "Message Sent",
      description: "Translation in progress...",
    });
  };

  const handleImageUpload = () => {
    toast({
      title: "Image Upload",
      description: "Image upload feature coming soon.",
    });
  };

  const handleClearHistory = () => {
    setRecords([]);
    toast({
      title: "History Cleared",
      description: "All translation records have been removed.",
    });
  };

  return (
    <div className="h-screen flex">
      <div className="w-1/3 min-w-[320px] max-w-md">
        <AvatarPanel isActive={isConversationActive || isRecording} />
      </div>
      
      <div className="flex-1 flex flex-col">
        <div className="flex-1 overflow-hidden">
          <TranscriptPanel records={records} />
        </div>
        
        <ControlArea
          mode={mode}
          onModeChange={setMode}
          isConversationActive={isConversationActive}
          onConversationToggle={handleConversationToggle}
          isRecording={isRecording}
          onRecordingToggle={handleRecordingToggle}
          onSendMessage={handleSendMessage}
          onImageUpload={handleImageUpload}
          onClearHistory={handleClearHistory}
        />
      </div>
    </div>
  );
}
