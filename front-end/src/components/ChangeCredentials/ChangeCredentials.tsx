import React from 'react';
import './ChangeCredentials.css';
import { Button, Form, Input } from 'antd';

const onFinishPassword = (values: any) => {
    console.log('Success:', values);
};

const onFinishEmail = (values: any) => {
    console.log('Success:', values);
};

const onFinishUsername = (values: any) => {
    console.log('Success:', values);
};

const onFinishFailed = (errorInfo: any) => {
  console.log('Failed operation');
};

type FieldTypePassword = {
    password?: string;
    oldPassword?: string;
    newPassword?: string;
};

type FieldTypeEmail = {
    email?: string;
    oldEmail?: string;
    newEmail?: string;
};

type FieldTypeUsername = {
    username?: string;
    oldUsername?: string;
    newUsername?: string;
};

const ChangeCredentials: React.FC = () => (
    <>
        <Form
            name="basic"
            labelCol={{ span: 8 }}
            wrapperCol={{ span: 16 }}
            style={{ maxWidth: 600 }}
            initialValues={{ remember: true }}
            onFinish={onFinishPassword}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
            className='change-credentials-form'
        >
            <Form.Item<FieldTypePassword>
            label="Old Password"
            name="oldPassword"
            id='old-password'
            rules={[{ required: true, message: 'Please input your old password!' }]}
            >
            <Input.Password />
            </Form.Item>

            <Form.Item<FieldTypePassword>
            label="New Password"
            name="newPassword"
            id='new-password'
            rules={[{ required: true, message: 'Please input your new password!' }]}
            >
            <Input.Password />
            </Form.Item>

            <Form.Item<FieldTypePassword>
            label="Confirm New Password"
            name="password"
            id='confirm-new-password'
            dependencies={['newPassword']}
            rules={[
                { required: true, message: 'Please confirm your new password!' },
                ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue('newPassword') === value) {
                        return Promise.resolve();
                      }
                      return Promise.reject(new Error('The new password that you entered do not match!'));
                    },
                  }),
            ]}
            >
            <Input.Password />
            </Form.Item>

            <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <Button type="primary" htmlType="submit">
                Change Password
            </Button>
            </Form.Item>
        </Form>
        <br />
        <Form
            name="basic"
            labelCol={{ span: 8 }}
            wrapperCol={{ span: 16 }}
            style={{ maxWidth: 600 }}
            initialValues={{ remember: true }}
            onFinish={onFinishEmail}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
            className='change-credentials-form-email'
        >
            <Form.Item<FieldTypeEmail>
            label="Old Email"
            name="oldEmail"
            id='old-email'
            rules={[{ required: true, message: 'Please input your old email!' }, { type: 'email', message: 'Please input a valid email!' }]}
            >
            <Input />
            </Form.Item>

            <Form.Item<FieldTypeEmail>
            label="New Email"
            name="newEmail"
            id='new-email'
            rules={[{ required: true, message: 'Please input your new email!' }, { type: 'email', message: 'Please input a valid email!' }]}
            >
            <Input />
            </Form.Item>

            <Form.Item<FieldTypeEmail>
            label="Confirm New Email"
            name="email"
            id='confirm-new-email'
            dependencies={['newEmail']}
            rules={[
                { required: true, message: 'Please confirm your new email!' }, 
                { type: 'email', message: 'Please input a valid email!' },
                ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue('newEmail') === value) {
                        return Promise.resolve();
                      }
                      return Promise.reject(new Error('The new email that you entered do not match!'));
                    },
                  }),
            ]}
            >
            <Input />
            </Form.Item>

            <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <Button type="primary" htmlType="submit">
                Change Email
            </Button>
            </Form.Item>
        </Form>
        <br />
        <Form
            name="basic"
            labelCol={{ span: 8 }}
            wrapperCol={{ span: 16 }}
            style={{ maxWidth: 600 }}
            initialValues={{ remember: true }}
            onFinish={onFinishUsername}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
            className='change-credentials-form-username'
        >
            <Form.Item<FieldTypeUsername>
            label="Old Username"
            name="oldUsername"
            id='old-username'
            rules={[{ required: true, message: 'Please input your old username!' }]}
            >
            <Input />
            </Form.Item>

            <Form.Item<FieldTypeUsername>
            label="New Username"
            name="newUsername"
            id='new-username'
            rules={[{ required: true, message: 'Please input your new username!' }]}
            >
            <Input />
            </Form.Item>

            <Form.Item<FieldTypeUsername>
            label="Confirm New Username"
            name="username"
            id='confirm-new-username'
            dependencies={['newUsername']}
            rules={[
                { required: true, message: 'Please confirm your new username!' },
                ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue('newUsername') === value) {
                        return Promise.resolve();
                      }
                      return Promise.reject(new Error('The new username that you entered do not match!'));
                    },
                  }),
            ]}
            >
            <Input />
            </Form.Item>

            <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <Button type="primary" htmlType="submit">
                Change Username
            </Button>
            </Form.Item>
        </Form>
    </>
  
);

export default ChangeCredentials;