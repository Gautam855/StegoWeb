"use client";
import React, { useState, useEffect } from "react";
import { HoveredLink, Menu, MenuItem } from "../../components/ui/navbar-menu";
import { cn } from "../../utils/cn";


export function NavbarDemo() {
    return (
      <div className="relative w-full flex items-center justify-center">
        <Navbar className="top-2" />
      </div>
    );
  }
  
  function Navbar({ className }: { className?: string }) {
    const [active, setActive] = useState<string | null>(null);
    return (
      <div
        className={cn("fixed top-10 inset-x-0 max-w-2xl mx-auto z-50", className)}
      >
        <Menu setActive={setActive}>
        <HoveredLink href="/">Home</HoveredLink>
          <MenuItem setActive={setActive} active={active} item="Encrypt">
            <div className="text-sm grid grid-cols-2 gap-10 p-4">
              <HoveredLink href="/EncryptImage">Image</HoveredLink>
              <HoveredLink href="/EncryptText">Text</HoveredLink>
            </div>
          </MenuItem>
          <MenuItem setActive={setActive} active={active} item="Decrypt">
            <div className="flex flex-col space-y-4 text-sm">
              <HoveredLink href="/DecryptImage">Image</HoveredLink>
              <HoveredLink href="/DecryptText">Text</HoveredLink>
              
            </div>
          </MenuItem>
  
          <HoveredLink href="/">Contact-us</HoveredLink>
          
        </Menu>
      </div>
    );
  }
  