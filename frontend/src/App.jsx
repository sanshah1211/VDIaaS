import React from 'react';
import Login from "./pages/Login.jsx"
import AdminDashboard from "./pages/admin-dashboard.jsx"
import Users from "./pages/Users.jsx"
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Groups from "./pages/Groups.jsx";



function App() {
  return (
      <BrowserRouter>
          <Routes>
              <Route path="/" element={<Login/>}/>
              <Route path="/admin" element={<AdminDashboard/>}/>
              <Route path="/users" element={<Users />}/>
              {/*<Route path="/create-groups" element={<Groups />}/>*/}
              <Route path="/groups" element={<Groups />}/>

              <Route path="/delete-groups" element={<Groups />}/>
          </Routes>
      </BrowserRouter>
  );
}

export default App
