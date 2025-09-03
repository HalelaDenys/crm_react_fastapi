import { useState } from "react";
import Sidebar from "./components/Sidebar/Sidebar";
import Main from "./components/Main/Main";

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen relative ">
      <button
        className={`lg:hidden absolute top-7 left-4 z-80 bg-gray-800 p-2 rounded 
          ${sidebarOpen ? "hidden" : ""}`}
        onClick={() => setSidebarOpen(!sidebarOpen)}
      >
        <img src="./menu.svg" alt="MenuIcon" className="w-5 h-5" />
      </button>

      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Основний контент */}
      <Main />
    </div>
  );
}

export default App;
