"use client";
import React, { useState, useEffect } from "react";
import { HoveredLink, Menu, MenuItem } from "../../components/ui/navbar-menu";
import { WavyBackground } from "../../components/ui/wavy-background";
import { cn } from "../../utils/cn";
import { BackgroundBeams} from "../../components/ui/background-beams";

function EncryptText() {
    useEffect(() => {
        // Any additional setup can be done here
      }, []);
    
      return (
        <div>
          <NavbarDemo />
          <BackgroundBeams/>
        </div>
      );
}


 
function BackgroundBeamsDemo() {
    return (
      <div className="h-[40rem] w-full rounded-md bg-neutral-950 relative flex flex-col items-center justify-center antialiased">
        <div className="max-w-2xl mx-auto p-4">
          <h1 className="relative z-10 text-lg md:text-7xl  bg-clip-text text-transparent bg-gradient-to-b from-neutral-200 to-neutral-600  text-center font-sans font-bold">
            Join the waitlist
          </h1>
          <p></p>
          <p className="text-neutral-500 max-w-lg mx-auto my-2 text-sm text-center relative z-10">
            Welcome to MailJet, the best transactional email service on the web.
            We provide reliable, scalable, and customizable email solutions for
            your business. Whether you&apos;re sending order confirmations,
            password reset emails, or promotional campaigns, MailJet has got you
            covered.
          </p>
          <input
            type="text"
            placeholder="hi@manuarora.in"
            className="rounded-lg border border-neutral-800 focus:ring-2 focus:ring-teal-500  w-full relative z-10 mt-4  bg-neutral-950 placeholder:text-neutral-700"
          />
        </div>
        <BackgroundBeams/>
      </div>
    );
  }


function NavbarDemo() {
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
          <MenuItem setActive={setActive} active={active} item="Home">
            
          </MenuItem>
          <MenuItem setActive={setActive} active={active} item="Encrypt">
            <div className="text-sm grid grid-cols-2 gap-10 p-4">
              <HoveredLink href="../about/page">Image</HoveredLink>
              <HoveredLink href="/Encrypt-Text">Text</HoveredLink>
            </div>
          </MenuItem>
          <MenuItem setActive={setActive} active={active} item="Decrypt">
            <div className="flex flex-col space-y-4 text-sm">
              <HoveredLink href="/Decrypt-Image">Image</HoveredLink>
              <HoveredLink href="/Decrypt-Text">Text</HoveredLink>
              
            </div>
          </MenuItem>
  
          <MenuItem setActive={setActive} active={active} item="Contact us">
          </MenuItem>
        </Menu>
      </div>
    );
  }
export default EncryptText;
