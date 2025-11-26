import TextInputArea from '../TextInputArea';

export default function TextInputAreaExample() {
  return (
    <TextInputArea 
      onSend={(text) => console.log('Send message:', text)}
      onImageUpload={() => console.log('Upload image triggered')}
    />
  );
}
