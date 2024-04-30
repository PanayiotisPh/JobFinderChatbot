import React, {useState} from 'react';
import './ChangeCredentials.css';
import { Button, Form, Input } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';

const ChangeCredentials: React.FC = () => {

    const navigate = useNavigate();
    const [url, setUrl] = useState('https://beetle-upward-yak.ngrok-free.app');



    interface PasswordFormValues {
        oldPassword: string;
        newPassword: string;
    }
    
    const onFinishPassword = async (values: PasswordFormValues) => {  

        try {
            // Make the API call
            console.log('Success:', values);

            const response = await fetch(`${url}/api/change-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`, // Ensure the token is correctly retrieved
                'ngrok-skip-browser-warning': 'true',
            },
            body: JSON.stringify({
                oldPassword: values.oldPassword,
                newPassword: values.newPassword,
                }),
            });

            if (!response.ok) {
                toast.error('Failed to change password. Please try again.', {
                    position: "top-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
            }

            const result = await response.json();

            if (response.status === 200) {
                navigate('/login',  { state: { fromCredentials: true } });
            } else if (response.status === 400) {
                toast.error( result, {
                    position: "top-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
            }

        } catch (error) {
            toast.error('Error changing password', {
                position: "top-right",
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
            });
        }

    };

    interface UsernameFormValues {
        oldUsername: string;
        newUsername: string;
    }
    
    const onFinishUsername = async (values: UsernameFormValues) => {  

        try {
            // Make the API call
            console.log('Success:', values);

            const response = await fetch(`${url}/api/change-username`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`, // Ensure the token is correctly retrieved
                'ngrok-skip-browser-warning': 'true',
            },
            body: JSON.stringify({
                oldUsername: values.oldUsername,
                newUsername: values.newUsername,
                }),
            });

            if (!response.ok) {
                toast.error('Failed to change username. Please try again.', {
                    position: "top-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
            }

            const result = await response.json();
            if (response.status === 200) {
                navigate('/login',  { state: { fromCredentials: true } });
            } else if (response.status === 400) {
                toast.error( result, {
                    position: "top-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
            }
        } catch (error) {
            toast.error('Error changing username', {
                position: "top-right",
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
            });
        }
        
    };
    
    const onFinishFailed = (errorInfo: any) => {
    console.log('Failed operation');
    };

    type FieldTypePassword = {
        password?: string;
        oldPassword?: string;
        newPassword?: string;
    };

    type FieldTypeUsername = {
        username?: string;
        oldUsername?: string;
        newUsername?: string;
    };

    return(
        <>
            <ToastContainer />
            <Form
                name="basic"
                labelCol={{ span: 8 }}
                wrapperCol={{ span: 16 }}
                initialValues={{ remember: true }}
                onFinish={onFinishPassword}
                onFinishFailed={onFinishFailed}
                autoComplete="off"
                style={{marginTop: "120px"}}
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
                <Button type="primary" htmlType="submit" className='button-style'>
                    Change Password
                </Button>
                </Form.Item>
            </Form>
            <br />
            <Form
                name="basic"
                labelCol={{ span: 8 }}
                wrapperCol={{ span: 16 }}
                initialValues={{ remember: true }}
                onFinish={onFinishUsername}
                onFinishFailed={onFinishFailed}
                autoComplete="off"
                className='change-credentials-form'
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
                <Button type="primary" htmlType="submit" className='button-style'>
                    Change Username
                </Button>
                </Form.Item>
            </Form>
        </>
    )
};

export default ChangeCredentials;