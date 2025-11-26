import { useState } from 'react';
import ControlArea from '../ControlArea';
import { Mode } from '../ModeSelector';

export default function ControlAreaExample() {
  const [mode, setMode] = useState<Mode>('conversation');
  const [isConversationActive, setIsConversationActive] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  
  return (
    <ControlArea
      mode={mode}
      onModeChange={setMode}
      isConversationActive={isConversationActive}
      onConversationToggle={() => setIsConversationActive(!isConversationActive)}
      isRecording={isRecording}
      onRecordingToggle={() => setIsRecording(!isRecording)}
      onSendMessage={(text) => console.log('Send:', text)}
      onImageUpload={() => console.log('Upload image')}
      onClearHistory={() => console.log('Clear history')}
    />
  );
}
