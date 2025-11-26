import { useState } from 'react';
import ModeSelector, { Mode } from '../ModeSelector';

export default function ModeSelectorExample() {
  const [mode, setMode] = useState<Mode>('conversation');
  
  return <ModeSelector mode={mode} onModeChange={setMode} />;
}
