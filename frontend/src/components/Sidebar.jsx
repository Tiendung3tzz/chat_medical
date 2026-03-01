import { useState, useEffect } from "react";
import "./Sidebar.css";
import { useNavigate } from "react-router-dom";

function Sidebar() {
  const navigate = useNavigate(); 
  const [disabledHover, setDisabledHover] =  useState(false);

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
    if (!disabledHover) {
      setDisabledHover(true);
    }
    if(n) {
      setDisabledHover(prev => !prev); 
    }
      // setDisabledHover(prev => !prev);      

    
  }
  return (
    <nav className="navigation">
      <div className={`nav-list nav-text ${disabledHover ? "expanded" : ""}`}>
        <div className="chat-ext">
          <div 
            className={`nav-item-1 ${!disabledHover ? "item-1-hover-1" : "item-1-hover-2"} ${disabledHover ? "nav-item-disabled" : ""}`} 
            onClick={() => handleClick()}
          >
            <img 
              src="/src/assets/add-post.png"
              alt="new chat" 
            />
            <div>New chat</div>
          </div>
          <img 
              src="/src/assets/app.png"
              className="img-2"
              onClick={() => handleClick(1)} 
              alt="close" 
          />
        </div>
        <hr />       
          <div className="nav-item-2" onClick={() => navigate('/')}>
            <img 
              src="/src/assets/messenger.png" 
              className="chat-ai" alt="chat ai" 
            />
            <div>Chat AI Health</div>
          </div>        
        <hr />
        {/* <div className="nav-item-3" onClick={() => navigate('/stthealth')}>
          <img src="/src/assets/hospital.png" className="check-health" alt="check health" />
          <div>Check health</div>
        </div>    
        <hr />
        {sessionStorage.getItem('token') ?
        <div className="nav-item-4" onClick={() => logout()}>
          <img src="/src/assets/exit.png" className="check-health" alt="check health" />
          <div>Log out</div>
        </div>  
        : null} */}
      </div>
      <div className="nav-text">
        {/* <h5>New chat</h5>
        <h5>Chat AI Health</h5>
        <h5>Check health</h5>
        <hr /> */}
      </div>
    </nav>
  )
}

export default Sidebar;