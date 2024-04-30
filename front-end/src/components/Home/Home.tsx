import React, { useState, useEffect } from 'react';
import './Home.css';
import { Drawer, Dropdown, Layout, Menu, MenuProps, Space } from 'antd';
import { DownOutlined, SearchOutlined  } from '@ant-design/icons';
import "react-chat-elements/dist/main.css"
import Sidebar from "../Sidebar/Sidebar";
import { useNavigate, Link, Outlet } from 'react-router-dom';


const Home: React.FC = () => {
  const { Header, Content, Footer, Sider } = Layout;
  const navigate = useNavigate();
  const [username, setUsername] = useState('User');
  const [url, setUrl] = useState('https://beetle-upward-yak.ngrok-free.app');


  const capitalizeFirstLetter = (string: string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  useEffect(() => {
    const fetchUsername = async () => {
      const token = localStorage.getItem('token'); // Assuming you store the JWT token in local storage
      try {
        const response = await fetch(`${url}/get-username`, {
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
        console.log(data);
        console.log(username);
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

  const [isSmallScreen, setIsSmallScreen] = useState(window.innerWidth < 600); 
  const [collapsed, setCollapsed] = useState(true);
  const [drawerVisible, setDrawerVisible] = useState(false);
  const toggleSidebar = () => {
    setCollapsed(!collapsed);
  };

  const toggleDrawer = () => {
    setDrawerVisible(!drawerVisible);
  };

  return (
    <Layout>
      {isSmallScreen ? (
        <Sider
            collapsible
            collapsed={collapsed}
            onCollapse={toggleSidebar}
            breakpoint="lg"
            collapsedWidth="0"
            width={200}
            className="site-layout-background"
            style={{ position: 'fixed', left: 0, zIndex: 1 }}
          >
          <Sidebar />
        </Sider>
      ): (
        <Sider width={200} className="site-layout-background">
          <Sidebar />
        </Sider>
      )}
      <Layout style={{ marginLeft: collapsed ? 0 : 200 }}>
        <Header className='header'>
        <div className='header-content'>
            {isSmallScreen ? (
              <SearchOutlined style={{ fontSize: '25px', color: '#fff', marginRight: '30px', marginTop: '10px' }} />
            ) : (
              <img src="/images/logo.png" alt='logo' className='logo-img-home' />
            )}
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