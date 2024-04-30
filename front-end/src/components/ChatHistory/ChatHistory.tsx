// ChatHistory.tsx
import React, { useState, useEffect, useRef } from 'react';
import './ChatHistory.css';
import { useParams } from 'react-router-dom'; // Import useParams

interface Message {
  text: string;
  user: 'user' | 'bot';
}

const ChatHistory: React.FC = () => {
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const { chatId } = useParams<{ chatId: string }>(); // Use useParams to get the session ID from the URL
  const [url, setUrl] = useState('https://beetle-upward-yak.ngrok-free.app');

  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const response = await fetch(`${url}/api/chat/${chatId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'ngrok-skip-browser-warning': 'true',
          },
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();

        // Ensure data is in the expected format (an array of messages)
        if (Array.isArray(data)) {
          setMessages(data);
        } else {
          console.error('Received data is not an array:', data);
          // Optionally handle the unexpected format, e.g., set an error state or messages to []
        }
      } catch (error) {
        console.error('Error fetching chat history:', error);
        // Optionally handle the fetch error, e.g., set an error state or messages to []
      }
    };

    if (chatId) {
      fetchChatHistory();
    }
  }, [chatId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chatbot-history-container">
      <div className="chatbot-history-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.user}`}>
            {msg.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatHistory;
