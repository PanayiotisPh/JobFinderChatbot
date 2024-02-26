import React, { useState, useEffect } from 'react';
import './Home.css';
import { Dropdown, Layout, Menu, MenuProps, Space } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import "react-chat-elements/dist/main.css"
import Sidebar from "../Sidebar/Sidebar";
import { useNavigate, Link, Outlet } from 'react-router-dom';


const Home: React.FC = () => {
  const { Header, Content, Footer, Sider } = Layout;
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
      label: <Link to="/change-credentials" style={{fontSize: "20px"}}>Change Credentials</Link>,
      key: '0',
    },
    {
      label: <div style={{fontSize: "20px"}} onClick={logout}>Log Out</div>,
      danger: true,
      key: '1',
    }
  ];


  return (
    <Layout>
      <Sider width={200} className="site-layout-background">
        <Sidebar />
      </Sider>
      <Layout style={{ paddingLeft: '200px' }}>
        <Header className='header'>
          <div className='header-content'>
            <img src="/images/logo.png" alt='logo' className='logo-img-home' />
            <div className='text'>Job Finder</div>
          </div>
          <Dropdown menu={{ items }} trigger={['click']}>
            <a onClick={(e) => e.preventDefault()}>
              <Space>
                <div style={{color: "white", padding: "10px", fontSize: "25px"}}>
                  {username}
                  <DownOutlined style={{color: "white", padding: "5px", fontSize: "21px"}}/>
                </div>
              </Space>
            </a>
          </Dropdown>
        </Header>
        <Content>
          <Outlet />
        </Content>
        <Footer style={{ textAlign: 'center' }}>Job Finder ©2024 Created by Panagiotis Fotiadis</Footer>
      </Layout>
    </Layout>
  );
};

export default Home;