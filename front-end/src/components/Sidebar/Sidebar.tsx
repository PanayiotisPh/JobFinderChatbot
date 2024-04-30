import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './Sidebar.css';
import { FiTrash2 } from 'react-icons/fi';
import { Popconfirm } from 'antd';


interface Session {
  chatId: string;
  date: string;
}

const Sidebar: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const navigate = useNavigate();
  const location = useLocation();
  const [url, setUrl] = useState(' https://beetle-upward-yak.ngrok-free.app');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
        navigate('/login');
    }
  }, []);
  
  useEffect(() => {
    const fetchSessions = async () => {
      const response = await fetch(`${url}/api/sessions`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'ngrok-skip-browser-warning': 'true',
        },
      });
      if (response.ok) {
        const data = await response.json();
        if (Array.isArray(data)) {
          setSessions(data);
        } else {
          console.error('Data is not an array:', data);
          // Handle non-array response here, for example, by setting sessions to an empty array
          setSessions([]);
        }
      } else {
        console.error('Failed to fetch sessions:', response.statusText);
        // Handle HTTP error here
      }
    };

    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    const response = await fetch(`${url}/api/sessions`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'ngrok-skip-browser-warning': 'true',
      },
    });
    if (response.ok) {
      const data = await response.json();
      if (Array.isArray(data)) {
        setSessions(data);
      } else {
        console.error('Data is not an array:', data);
        // Handle non-array response here, for example, by setting sessions to an empty array
        setSessions([]);
      }
    } else {
      console.error('Failed to fetch sessions:', response.statusText);
      // Handle HTTP error here
    }
  };

  const handleSessionClick = (sessionId: string) => {
    navigate(`/chat/${sessionId}`);
  };

  const isActiveSession = (chatId: string) => {
    return location.pathname === `/chat/${chatId}`;
  };

  const isCurrentChatActive = () => {
    return location.pathname === "/"; // Check if the current pathname is the home page
  };

  const handleDeleteSession = async (chatId: string) => {
    // API call to delete the session
    const response = await fetch(`${url}/api/chat/${chatId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'ngrok-skip-browser-warning': 'true',
      },
    });
    if (response.ok) {
      // If the deletion was successful, refetch the sessions to update the UI
      fetchSessions();
    } else {
      console.error('Failed to delete session');
    }
  };

  const refreshChat = async () => {
    const response = await fetch(`${url}/reset_rasa`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'ngrok-skip-browser-warning': 'true',
      },
    });
    if (response.ok) {
      window.location.reload();
    } else {
      console.error('Failed to delete session');
    }
  };

  const isCvActive = () => {
    return location.pathname === "/cv-details"; // Check if the current pathname is the home page
  };

  return (
    <>
      <div className="sidebar">
        <div className='refresh-chat-button' onClick={() => refreshChat()}>
          Refresh Chat
        </div>
        <Link to="/cv-details" className={`sidebar-link ${isCvActive() ? "activeSession" : ""}`}>
          Resume/CV Details
        </Link>
        <Link to="/" className={`sidebar-link ${isCurrentChatActive() ? "activeSession" : ""}`}>
          New Chat
        </Link>
        {sessions.map(session => (
        <div
          key={session.chatId}
          onClick={() => handleSessionClick(session.chatId)}
          className={isActiveSession(session.chatId) ? "activeSession" : ""}
        >
          <div className="session-item" onClick={() => handleSessionClick(session.chatId)}>
            <div className="session-date">{new Date(session.date).toLocaleDateString()}</div>
            <Popconfirm
              title="Delete chat"
              description="Are you sure to delete this chat?"
              okText="Yes"
              cancelText="No"
              onConfirm={() => handleDeleteSession(session.chatId)}
            >
              <FiTrash2 className="trash-icon" />
            </Popconfirm>
          </div>
        </div>
      ))}
      </div>
    </>
  );
};

export default Sidebar;
