import { useState, useEffect } from "react";
import "./Sidebar.css";
import { useNavigate } from "react-router-dom";

// 👉 import ảnh
import addPost from "@/assets/add-post.png";
import appIcon from "@/assets/app.png";
import messenger from "@/assets/messenger.png";

function Sidebar() {
  const navigate = useNavigate(); 
  const [disabledHover, setDisabledHover] = useState(false);

  useEffect(() => {
    const cls = "nav-expanded";
    if (disabledHover) {
      document.body.classList.add(cls);
    } else {
      document.body.classList.remove(cls);
    }
    return () => document.body.classList.remove(cls);
  }, [disabledHover]);

  const handleClick = (n) => {
    if (!disabledHover) setDisabledHover(true);
    if (n) setDisabledHover(prev => !prev);
  };

  return (
    <nav className="navigation">
      <div className={`nav-list nav-text ${disabledHover ? "expanded" : ""}`}>
        <div className="chat-ext">
          <div
            className={`nav-item-1 ${!disabledHover ? "item-1-hover-1" : "item-1-hover-2"} ${disabledHover ? "nav-item-disabled" : ""}`}
            onClick={() => handleClick()}
          >
            <img src={addPost} alt="new chat" />
            <div>New chat</div>
          </div>

          <img
            src={appIcon}
            className="img-2"
            onClick={() => handleClick(1)}
            alt="close"
          />
        </div>

        <hr />

        <div className="nav-item-2" onClick={() => navigate("/")}>
          <img
            src={messenger}
            className="chat-ai"
            alt="chat ai"
          />
          <div>Chat AI Health</div>
        </div>

        <hr />
      </div>
    </nav>
  );
}

export default Sidebar;