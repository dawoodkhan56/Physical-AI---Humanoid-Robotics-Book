import React, { useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import BookChatbot from '@site/src/components/BookChatbot';

// This component will render the BookChatbot on every page
export default function ChatbotInjector() {
  const location = useLocation();
  
  // Show chatbot on all pages except excluded paths
  const showChatbot = !location.pathname.includes('/chat') && 
                     !location.pathname.includes('/playground');
  
  return showChatbot ? <BookChatbot /> : null;
}