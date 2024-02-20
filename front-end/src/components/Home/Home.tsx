import React, { useState, useEffect } from 'react';
import './Home.css';
import { Dropdown, Layout, Menu, MenuProps, Space } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import "react-chat-elements/dist/main.css"
import Chat from "../Chat/Chat";
import { useNavigate } from 'react-router-dom';


const Home: React.FC = () => {
  const { Header, Content, Footer } = Layout;
  const navigate = useNavigate();
  const [username, setUsername] = useState('User');

  const capitalizeFirstLetter = (string: string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  useEffect(() => {
    const fetchUsername = async () => {
      const token = localStorage.getItem('token'); // Assuming you store the JWT token in local storage
      try {
        const response = await fetch('http://127.0.0.1:5000/get-username', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setUsername(capitalizeFirstLetter(data));
      } catch (error) {
        console.error("Could not fetch username:", error);
      }
    };

    fetchUsername();
  }, []);

  const logout = () => {
    localStorage.removeItem('token'); // Clear the token from localStorage
    navigate('/login');
  };

  const items: MenuProps['items'] = [
    {
      label: <div style={{fontSize: "20px"}} onClick={logout}>Log Out</div>,
      danger: true,
      key: '0',
    },
  ];


  return (
    <Layout>

      <Header className='header'>
        <div>
          <img src="/images/logo.png" alt='logo' className='logo-img-home' />
        </div>
        <div className='text'>Job Finder</div>
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['2']}
          // items={items}
          style={{ flex: 1, minWidth: 0 }}
        />

        <Dropdown menu={{ items }} trigger={['click']}>
          <a onClick={(e) => e.preventDefault()}>
          <Space>
            <div style={{color: "white", padding: "10px", fontSize: "20px"}}>
              {username}
              <DownOutlined style={{color: "white", padding: "5px", fontSize: "20px"}}/>
            </div>
          </Space>
          </a>
        </Dropdown>

      </Header>


      <Content>
        <Chat />
      </Content>

      <Footer style={{ textAlign: 'center' }}>Job Finder ©2024 Created by Panagiotis Fotiadis</Footer>

    </Layout>
  );
};

export default Home;