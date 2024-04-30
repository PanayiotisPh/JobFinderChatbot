import React, { useState, useEffect } from 'react';
import './CvDetails.css';
import { InboxOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { message, Upload, Divider, List, Input, } from 'antd';
import type { RcFile } from 'antd/lib/upload';
import Search from 'antd/es/input/Search';
import { FaGithub } from 'react-icons/fa';

const { Dragger } = Upload;

const CvDetails: React.FC = () => {
    const [softskills, setSoftskills] = useState<string[]>([]);
    const [hardskills, setHardskills] = useState<string[]>([]);
    const [githubskills, setGithubskills] = useState<string[]>([]);
    const [url, setUrl] = useState('https://beetle-upward-yak.ngrok-free.app');


    const fetchSoftSkills = async () => {
        try {
            const response = await fetch(`${url}/get-cv-soft-skills`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'ngrok-skip-browser-warning': 'true',
                }, 
            });

            if (!response.ok) {
                throw new Error('Failed to fetch soft skills');
            }

            const data = await response.json();
            setSoftskills(data); // Assuming the response has a 'softskills' field
        } catch (error) {
            console.error('Error fetching soft skills:', error);
            message.error('Failed to load soft skills');
        }
    };

    // useEffect hook to fetch soft skills on component mount
    useEffect(() => {
        fetchSoftSkills();
    }, []);

    const fetchHardSkills = async () => {
        try {
            const response = await fetch(`${url}/get-cv-hard-skills`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'ngrok-skip-browser-warning': 'true',
                }, 
            });

            if (!response.ok) {
                throw new Error('Failed to fetch soft skills');
            }

            const data = await response.json();
            setHardskills(data); // Assuming the response has a 'softskills' field
        } catch (error) {
            console.error('Error fetching soft skills:', error);
            message.error('Failed to load soft skills');
        }
    };

    // useEffect hook to fetch soft skills on component mount
    useEffect(() => {
        fetchHardSkills();
    }, []);
        
    const fetchGithubSkills = async (username: string) => {
        try {
            const response = await fetch(`${url}/info_github`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                    'ngrok-skip-browser-warning': 'true',
                },
                body: JSON.stringify({ username }),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch github skills');
            }

            const data = await response.json();
            setGithubskills(data); // Assuming the response has a 'githubskills' field
        } catch (error) {
            console.error('Error fetching github skills:', error);
            message.error('Failed to load github skills');
        }
    }

    const fetchGithubSkillsOnLoad = async () => {
        try {
            const response = await fetch(`${url}/get_github`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'ngrok-skip-browser-warning': 'true',
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch github skills');
            }

            const data = await response.json();
            setGithubskills(data);
        } catch (error) {
            console.error('Error fetching github skills:', error);
            message.error('Failed to load github skills');
        }
    }

    // useEffect hook to fetch github skills on component mount
    useEffect(() => {
        fetchGithubSkillsOnLoad();
    }, []);

    const handleFileUpload = async (file: File) => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${url}/analyse-text`, {
                method: 'POST',
                body: formData,
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'ngrok-skip-browser-warning': 'true',
                  },            
                });

            if (response.ok) {
                const data = await response.json();
                message.success(`${file.name} file analyzed successfully.`);
                setSoftskills(data.soft_skills);
                setHardskills(data.hard_skills);
            } else {
                message.error(`${file.name} file analysis failed.`);
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            message.error('Error uploading file');
        }
    };

    const props: UploadProps = {
        name: 'file',
        multiple: false,
        action: '', // This will be ignored since we are handling file upload manually
        maxCount: 1,
        beforeUpload(file) {
            const isPdfOrDocx = file.type === 'application/pdf' || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
            if (!isPdfOrDocx) {
                message.error('You can only upload PDF or DOCX file!');
                return Upload.LIST_IGNORE;
            }
            return true; // Prevent automatic upload
        },
        customRequest: ({ file, onSuccess, onError }) => {
            handleFileUpload(file as RcFile)
                .then(() => onSuccess?.(file))
                .catch(onError);
            return {
                abort() {
                    console.log('Upload aborted');
                },
            };
        },
        onDrop(e) {
            console.log('Dropped files', e.dataTransfer.files);
        },
    };

    return (
        <div>
            <div className='title'>
                Any CV you upload will be analyzed and the soft and hard skills will be displayed below.
                Those skills will be used along with the details you provide in the chat to match you with the best job offers.
            </div>
            <div className='upload'>
                <Dragger {...props}>
                    <p className="ant-upload-drag-icon">
                        <InboxOutlined />
                    </p>
                    <p className="ant-upload-text">Click or drag file to this area to upload</p>
                    <p className="ant-upload-hint">
                        Support for a single upload of .pdf or .docx .
                    </p>
                </Dragger>
            </div>
            <div className='upload'>
                <Search 
                    placeholder="Github Username" 
                    prefix={<FaGithub style={{ marginRight: '10px' }} />} 
                    style={{ width: 200, margin: 10 }}
                    onSearch={(value) => fetchGithubSkills(value)}
                />
            </div>
            <div className='lists'>
                <div>
                    <div style={{fontSize: 20, fontWeight: 'bold', marginBottom: 5, marginRight: 15}}>Soft Skills Detected</div>
                    <List
                        size="small"
                        bordered
                        pagination={{ pageSize: 10 }}
                        dataSource={softskills}
                        renderItem={(item) => <List.Item>{item}</List.Item>}
                        className='list'
                    />
                </div>
                <div>
                    <div style={{fontSize: 20, fontWeight: 'bold', marginBottom: 5, marginRight: 15}}>Hard Skills Detected</div>
                    <List
                        size="small"
                        bordered
                        pagination={{ pageSize: 10 }}
                        dataSource={hardskills}
                        renderItem={(item) => <List.Item>{item}</List.Item>}
                        className='list'
                    />
                </div>
                <div>
                    <div style={{fontSize: 20, fontWeight: 'bold', marginBottom: 5}}>Languages Detected on Github</div>
                    <List
                        size="small"
                        bordered
                        pagination={{ pageSize: 10 }}
                        dataSource={githubskills}
                        renderItem={(item) => <List.Item>{item}</List.Item>}
                        className='list'
                    />
                </div>
            </div>
        </div>
    );
};

export default CvDetails;
