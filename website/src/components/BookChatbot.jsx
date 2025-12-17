import React, { useState, useRef, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import '../css/chatbot.css';

const BookChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [isSelecting, setIsSelecting] = useState(false);
  const messagesEndRef = useRef(null);
  const location = useLocation();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Listen for text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection.toString().trim() !== '') {
        const text = selection.toString();
        if (text.length > 2) {  // Only consider meaningful selections
          setSelectedText(text);
          setIsSelecting(true);
          setTimeout(() => setIsSelecting(false), 5000); // Hide after 5 seconds
        }
      }
    };

    const handleMouseUp = () => {
      setTimeout(handleSelection, 0); // Allow selection to complete
    };

    document.addEventListener('mouseup', handleMouseUp);
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: newMessages,
          selected_text: selectedText,
          context: {
            current_page: location.pathname,
            current_section: document.title
          }
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const data = await response.json();

      // Add assistant message with sources if available
      const assistantMessage = {
        role: 'assistant',
        content: data.response,
        sources: data.sources || []
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.message || 'Please try again.'}`,
        sources: []
      }]);
    } finally {
      setIsLoading(false);
      setSelectedText(''); // Clear selection after sending
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const askAboutSelection = () => {
    if (selectedText) {
      setInput(`Explain this: "${selectedText.substring(0, 100)}${selectedText.length > 100 ? '...' : ''}"`);
      setSelectedText('');
    }
  };

  // Render message with sources if available
  const renderMessage = (msg, index) => {
    return (
      <div key={index} className={`message ${msg.role}`}>
        <div className="message-content">{msg.content}</div>
        {msg.sources && msg.sources.length > 0 && (
          <div className="sources">
            <h4>References:</h4>
            <ul>
              {msg.sources.map((source, idx) => (
                <li key={idx}>
                  <a href={source.url} target="_blank" rel="noopener noreferrer">
                    {source.title || source.url}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className={`chatbot-container ${isOpen ? 'open' : 'closed'}`}>
      {!isOpen ? (
        <button
          className="chatbot-toggle"
          onClick={() => setIsOpen(true)}
          aria-label="Open chatbot"
        >
          💬
        </button>
      ) : (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>Book Assistant</h3>
            <button
              className="chatbot-close"
              onClick={() => setIsOpen(false)}
              aria-label="Close chatbot"
            >
              ×
            </button>
          </div>

          {selectedText && isSelecting && (
            <div className="selection-quick-action">
              <button onClick={askAboutSelection}>
                Ask about selected text: "{selectedText.substring(0, 30)}..."
              </button>
            </div>
          )}

          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <p>Hello! I'm your Physical AI & Humanoid Robotics assistant.</p>
                <p>Ask me questions about the content, or select text and click the button to ask about it.</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                renderMessage(msg, index)
              ))
            )}
            {isLoading && (
              <div className="message assistant">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-input">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question about Physical AI & Humanoid Robotics..."
              disabled={isLoading}
              rows={2}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default BookChatbot;