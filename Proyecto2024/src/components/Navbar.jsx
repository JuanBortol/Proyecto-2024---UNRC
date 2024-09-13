import React, { useState } from "react";
import DarkModeButton from "./DarkModeButton";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="bg-transparent fixed top-0 w-full">
      <div className="container text-white mx-auto flex justify-between items-center p-2">
        <div className="text-white text-4xl font-bold">PROTEINA</div>
        
        {/* Desktop Menu */}
        <div className="hidden md:flex space-x-8 font-thin items-center">
          <a href="#" className="text-sm">reportar</a>
        <a href="#" className="text-sm">historial</a>
        <button className='bg-white rounded-full py-2 px-8 text-green-950 font-light'>
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
            <a href="#" className="block text-3xl">about</a>
            <a href="#" className="block text-3xl">reportar</a>
            <a href="#" className="block text-3xl">historial</a>
            <a href="#" className="block text-3xl">logout</a>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
