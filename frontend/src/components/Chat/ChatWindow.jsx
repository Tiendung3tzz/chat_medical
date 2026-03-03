import { useState } from "react";
import ChatInput from "./ChatInput";
import "./Chat.css";

export default function Content() {
  const [messages, setMessages] = useState([]);

  const sendAnswerAPI = async (text) => {
    try {
      const response = await fetch("http://54.252.187.59:8000/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: text }),
      });

      if (!response.ok) {
        throw new Error("API error");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        { type: "bot", content: data.answer },
      ]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        { type: "bot", content: "Có lỗi xảy ra. Vui lòng thử lại." },
      ]);
    }
  };

  const handleSend = (text) => {
    setMessages((prev) => [
      ...prev,
      { type: "user", content: text }
    ]);

    
    sendAnswerAPI(text);
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