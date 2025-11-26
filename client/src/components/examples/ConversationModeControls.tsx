import { useState } from 'react';
import ConversationModeControls from '../ConversationModeControls';

export default function ConversationModeControlsExample() {
  const [isActive, setIsActive] = useState(false);
  
  return (
    <ConversationModeControls 
      isActive={isActive} 
      onToggle={() => setIsActive(!isActive)} 
    />
  );
}
