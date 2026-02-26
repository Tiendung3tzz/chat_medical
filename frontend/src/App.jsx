import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/Chat/ChatWindow.jsx";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";

function App() {
  return (
    <div className="app">
      <Router>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Sidebar />
                <ChatWindow />
              </>
            }
          />
        </Routes>
      </Router>
      
    </div>
  );
}

export default App;