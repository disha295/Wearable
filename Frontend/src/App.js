import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Dashboards from "./pages/Dashboards";
import Nudges from "./pages/Nudges";

function App() {
  return (
    <Router>
      <header className="bg-white shadow-sm border-b border-gray-200 mb-6">
        <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
          <h1 className="text-lg font-semibold text-gray-800">HeartTrend</h1>
          <nav className="flex space-x-6 text-sm font-medium text-gray-600">
            <Link to="/" className="hover:text-blue-600 transition">
              Home
            </Link>
            <Link to="/dashboards" className="hover:text-blue-600 transition">
              Dashboards
            </Link>
            <Link to="/nudges" className="hover:text-blue-600 transition">
              Nudges
            </Link>
          </nav>
        </div>
      </header>

      <main className="px-4 max-w-7xl mx-auto">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboards" element={<Dashboards />} />
          <Route path="/nudges" element={<Nudges />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
