import React from 'react';
import './Home.css';
import { Dropdown, Layout, Menu, MenuProps, Space } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import "react-chat-elements/dist/main.css"
import Chat from "../Chat/Chat";

const { Header, Content, Footer } = Layout;

const items: MenuProps['items'] = [
  {
    label: <div style={{fontSize: "20px"}}>Log Out</div>,
    danger: true,
    key: '0',
  },
];

const Home: React.FC = () => {

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
              <div style={{color: "white", padding: "px", fontSize: "20px"}}>
                User
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