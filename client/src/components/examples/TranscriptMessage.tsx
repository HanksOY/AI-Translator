import TranscriptMessage from '../TranscriptMessage';

export default function TranscriptMessageExample() {
  return (
    <TranscriptMessage
      sourceText="Hello, how can I help you today?"
      translatedText="Bonjour, comment puis-je vous aider aujourd'hui?"
      sourceLanguage="EN"
      targetLanguage="FR"
      timestamp="2:45 PM"
    />
  );
}
