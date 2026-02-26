function MessageItem({ message }) {
  return (
    <div className={`message ${message.role}`}>
      <div className="message-content">
        {message.content}
      </div>
    </div>
  );
}

export default MessageItem;