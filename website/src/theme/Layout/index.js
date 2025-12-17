import React from 'react';
import Layout from '@theme-original/Layout';
import BookChatbot from '@site/src/components/BookChatbot';
import { useLocation } from '@docusaurus/router';

export default function LayoutWrapper(props) {
  const location = useLocation();
  
  // Show chatbot on all pages except the chatbot page itself if it exists
  const showChatbot = !location.pathname.includes('/chat') && 
                     !location.pathname.includes('/playground');
  
  return (
    <>
      <Layout {...props}>
        {props.children}
      </Layout>
      {showChatbot && <BookChatbot />}
    </>
  );
}