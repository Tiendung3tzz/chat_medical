import { useState } from "react";
import ChatInput from "./ChatInput";
import "./Chat.css";

export default function Content() {
  const [messages, setMessages] = useState([]);

  const handleSend = (text) => {
    setMessages((prev) => [
      ...prev,
      { type: "user", content: text }
    ]);

    // Sau này bật lại API
    // sendAnswerAPI(text);
  };

  return (
    <div className="content-container">
      <div className="message">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={msg.type === "user" ? "user-message" : "bot-message"}
          >
            <p>{msg.content}</p>
          </div>
        ))}
      </div>

      <ChatInput onSend={handleSend} />
    </div>
  );
}