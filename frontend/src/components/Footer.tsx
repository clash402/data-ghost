import React from 'react';

const Footer = () => (
  <footer className="w-full py-4 px-4 border-t bg-background text-xs text-muted-foreground flex flex-col items-center gap-1">
    <span>&copy; {new Date().getFullYear()} Josh Courtney. All rights reserved.</span>
    <div className="flex gap-4">
      <a href="https://joshcourtney.com/" target="_blank" rel="noopener noreferrer" className="hover:underline">My Site</a>
      <a href="https://github.com/clash402" target="_blank" rel="noopener noreferrer" className="hover:underline">GitHub</a>
      <a href="https://www.linkedin.com/in/joshcourtney402/" target="_blank" rel="noopener noreferrer" className="hover:underline">LinkedIn</a>
    </div>
  </footer>
);

export default Footer; 