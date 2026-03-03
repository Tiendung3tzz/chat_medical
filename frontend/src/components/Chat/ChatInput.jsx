import { useState } from "react";
import "./Chat.css";

import addIcon from "@/assets/add.png";
import loginIcon from "@/assets/login.png";

export default function ChatInput({ onSend }) {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    const trimmedMessage = message.trim();
    if (!trimmedMessage) return;
    onSend(trimmedMessage);
    setMessage("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="input-container">
      <img src={addIcon} className="item-input" alt="add" />

      <textarea
        className="text-input"
        placeholder="Are you question..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      <img
        src={loginIcon}
        className="item-input"
        id="enter"
        alt="enter"
        onClick={handleSend}
      />
    </div>
  );
}