import React, { useState } from 'react';
import { MessageBox, Input, Button } from 'react-chat-elements';
import axios from 'axios';

function Chat() {
    const [message, setMessage] = useState('');
    const [chatHistory, setChatHistory] = useState([] as any[]); // Provide an initial value for chatHistory

    const sendMessage = async () => {
        if (!message) return;

        const userMessage = {
            position: 'right',
            type: 'text',
            text: message,
            date: new Date(),
        };

        try {
            const response = await axios.post('http://localhost:5005/webhooks/rest/webhook', {
                sender: 'user',
                message: message,
            });

            response.data.forEach((msg: any) => {
                const botMessage = {
                    position: 'left',
                    type: 'text',
                    text: msg.text,
                    date: new Date(),
                };

                setChatHistory((prevHistory) => [...prevHistory, botMessage]);
            });
        } catch (error) {
            console.error('Error:', error);
        }

        setMessage('');
    };

    return (
        <div>
            {chatHistory.map((msg, index) => (
                <MessageBox key={index} {...msg} />
            ))}
            <Input
                placeholder="Type here..."
                value={message}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setMessage(e.target.value)}
                maxHeight = { 200 } // Add this line
                rightButtons={
                    <Button
                        color="white"
                        backgroundColor="black"
                        text="Send"
                        onClick={sendMessage}
                    />
                }
            />

        </div>
    );
}

export default Chat;
