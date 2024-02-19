// Chatbot.tsx
import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';

interface Message {
  text: string;
  user: 'user' | 'bot';
}

const Chat: React.FC = () => {
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const [isLoading, setIsLoading] = useState(false);

  const [messages, setMessages] = useState<Message[]>([
    { text: "Say 'hi' to start the conversation!!!", user: 'bot' },
  ]);
  const [input, setInput] = useState<string>('');

  const sendToRasa = async (userMessage: string): Promise<Message[]> => {
    try {
      const rasaEndpoint = 'http://localhost:5005/webhooks/rest/webhook';
      const response = await fetch(rasaEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sender: 'user',
          message: userMessage,
        }),
      });
  
      const data = await response.json();
  
      // Transform all responses from Rasa into Message objects
      const botReplies: Message[] = data.map((reply: any) => ({
        text: reply.text,
        user: 'bot',
      }));
  
      return botReplies;
    } catch (error) {
      console.error('Error sending message to Rasa:', error);
      return [{ text: 'Error communicating with the bot.', user: 'bot' }];
    }
  };
  
  


  const handleSendMessage = async () => {
    if (input.trim() !== '') {
      setIsLoading(true);
      const userMessage: Message = { text: input, user: 'user' };
      const botResponses: Message[] = await sendToRasa(input);
  
      // Update state with the user message and all bot responses
      setMessages((prevMessages) => [
        ...prevMessages,
        userMessage,
        ...botResponses,
      ]);
  
      setInput('');
      setIsLoading(false);
    }
  };
  
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);
  
  
  return (
    <div className="chatbot-container">
      <div className="chatbot-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.user}`}>
            {msg.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="chatbot-input">
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey && !isLoading) { // Prevent sending on Shift + Enter
              e.preventDefault(); // Prevent the default action to avoid submitting the form (if any)
              handleSendMessage();
            }
          }}
          disabled={isLoading}
        />
        <button onClick={handleSendMessage} disabled={isLoading}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
