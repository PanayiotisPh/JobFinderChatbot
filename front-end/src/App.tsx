import React from 'react';
import './index.css';
import { Dropdown, Flex, Layout, Menu, MenuProps, Space, theme } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import "react-chat-elements/dist/main.css"
import Chat from "./components/Chat";

const { Header, Content, Footer } = Layout;

// const items = new Array(15).fill(null).map((_, index) => ({
//   key: index + 1,
//   label: `nav ${index + 1}`,
// }));

const items: MenuProps['items'] = [
  {
    label: <div style={{fontSize: "20px"}}>Log Out</div>,
    danger: true,
    key: '0',
  },
];

const App: React.FC = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  return (
    <Layout>

      <Header style={{ display: 'flex', alignItems: 'center', minHeight: '100px' }}>
        <div>
          <img src="\images\logo.png" style={{ marginTop:'20px' ,maxHeight: '100%', maxWidth: '130px', height: 'auto', width: 'auto' }} />
        </div>
        <div style={{ color:'white', fontSize: '30px' }}>Job Finder</div>
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

      <Footer style={{ textAlign: 'center', paddingTop: '9%' }}>
        Panagiotis Fotiadis ©{new Date().getFullYear()}
      </Footer>

    </Layout>
  );
};

export default App;