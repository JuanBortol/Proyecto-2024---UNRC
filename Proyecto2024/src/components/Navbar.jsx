import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import DarkModeButton from "./DarkModeButton";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const handleHome = () => {navigate('/home')}
  const handleLogout = () => {navigate('/logout');}
  const handleHistory = () => {navigate('/history');}

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="bg-transparent fixed top-0 w-full">
      <div className="container text-white mx-auto flex justify-between items-center p-2">
      <button className="text-white text-4xl font-bold bg-transparent border-none cursor-pointer focus:outline-none"
      onClick={handleHome}>
        PROTEINA
      </button>
        
        {/* Desktop Menu */}
        <div className="hidden md:flex space-x-8 font-thin items-center">
          <a className="text-sm cursor-pointer">reportar</a>
        <a className="text-sm cursor-pointer" onClick={handleHistory}>historial</a>
        <button className='bg-white rounded-full py-2 px-8 text-green-950 font-light' onClick={handleLogout}>
        logout
        </button>
        <DarkModeButton
        height='28px' className="size-8"
        ></DarkModeButton>
        </div>
        
        {/* Mobile Menu Button */}
        <button 
          className="md:hidden text-white focus:outline-none
          font-bold text-xl px-4" 
          onClick={toggleMenu}>
          ☰
        </button>
      </div>
      
      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden space-y-8 py-6 text-center text-white font-extralight">
            <a href="#" className="block text-3xl">reportar</a>
            <a href="#" className="block text-3xl">historial</a>
            <a href="#" className="block text-3xl" onClick={handleLogout}>logout</a>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
