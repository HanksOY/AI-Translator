import TranscriptPanel from '../TranscriptPanel';

export default function TranscriptPanelExample() {
  const mockRecords = [
    {
      id: '1',
      sourceText: 'Good morning, I would like to discuss the financial report.',
      translatedText: 'Buenos días, me gustaría discutir el informe financiero.',
      sourceLanguage: 'EN',
      targetLanguage: 'ES',
      timestamp: new Date(Date.now() - 300000),
    },
    {
      id: '2',
      sourceText: 'What are the key performance indicators for this quarter?',
      translatedText: '¿Cuáles son los indicadores clave de rendimiento para este trimestre?',
      sourceLanguage: 'EN',
      targetLanguage: 'ES',
      timestamp: new Date(Date.now() - 180000),
    },
    {
      id: '3',
      sourceText: 'The revenue growth has exceeded our projections.',
      translatedText: 'El crecimiento de los ingresos ha superado nuestras proyecciones.',
      sourceLanguage: 'EN',
      targetLanguage: 'ES',
      timestamp: new Date(Date.now() - 60000),
    },
  ];

  return <TranscriptPanel records={mockRecords} />;
}
