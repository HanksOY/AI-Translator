import { useState } from 'react';
import ConventionModeControls from '../ConventionModeControls';

export default function ConventionModeControlsExample() {
  const [isRecording, setIsRecording] = useState(false);
  
  return (
    <ConventionModeControls 
      isRecording={isRecording} 
      onToggle={() => setIsRecording(!isRecording)} 
    />
  );
}
