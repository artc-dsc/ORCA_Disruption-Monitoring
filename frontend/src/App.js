import React from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import './assets/scss/themes.scss';
import Homepage from "./pages/Homepage";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Homepage />} />
      </Routes>
    </Router>
  );
};

export default App;