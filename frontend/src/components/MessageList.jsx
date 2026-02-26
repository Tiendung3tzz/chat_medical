import MessageItem from "./MessageItem";

function MessageList({ messages }) {
  return (
    <div className="message-list">
      {messages.map((msg) => (
        <MessageItem key={msg.id} message={msg} />
      ))}
    </div>
  );
}

export default MessageList;