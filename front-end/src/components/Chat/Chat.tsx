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
  const [url, setUrl] = useState('https://beetle-upward-yak.ngrok-free.app');


  const [messages, setMessages] = useState<Message[]>([
    { text: "Say 'hi' to start the conversation!!!", user: 'bot' },
  ]);
  const [input, setInput] = useState<string>('');

  const sendToRasa = async (userMessage: string): Promise<Message[]> => {
    try {
      // Your Flask API endpoint for forwarding messages to Rasa
      const apiEndpoint = `${url}/api/messages`;
      const token = localStorage.getItem('token'); // Retrieve JWT from local storage
  
      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // Include the JWT in the request
        },
        body: JSON.stringify({
          message: userMessage,
        }),
      });
  
      const data = await response.json();
  
      // Transform the responses from your Flask API into Message objects
      const botReplies: Message[] = data.map((reply: any) => ({
        text: reply.text,
        user: 'bot',
      }));
  
      return botReplies;
    } catch (error) {
      console.error('Error sending message through API:', error);
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

      const shouldSaveConversation = botResponses.some(response => response.text === "To start over, type 'hi'.");
      if (shouldSaveConversation) {
        saveConversation([...messages, userMessage, ...botResponses]);
      }
    
      setInput('');
      setIsLoading(false);
    }
  };
  
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);
  
  const saveConversation = async (conversation: Message[]) => {
    try {
      const apiEndpoint = `${url}/save-chat`;
      const token = localStorage.getItem('token'); // Retrieve JWT from local storage
  
      await fetch(apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // Include the JWT in the request
        },
        body: JSON.stringify({
          messages: conversation,
        }),
      });
  
      console.log('Conversation saved successfully');
    } catch (error) {
      console.error('Error saving conversation:', error);
    }
  };
  
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
