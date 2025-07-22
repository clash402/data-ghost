import React from 'react';

export default function Footer() {
  return (
    <footer className="w-full py-3 sm:py-4 px-4 sm:px-6 lg:px-8 border-t border-slate-200 dark:border-slate-700 bg-white/10 dark:bg-slate-800/10 backdrop-blur-sm text-xs sm:text-sm text-slate-600 dark:text-slate-400 flex flex-col items-center gap-1 transition-all duration-300">
      <span>&copy; {new Date().getFullYear()} Josh Courtney. All rights reserved.</span>
      <div className="flex gap-3 sm:gap-4">
        <a href="https://joshcourtney.com/" target="_blank" rel="noopener noreferrer" className="hover:underline hover:text-slate-800 dark:hover:text-slate-200 transition-colors duration-300">My Site</a>
        <a href="https://github.com/clash402" target="_blank" rel="noopener noreferrer" className="hover:underline hover:text-slate-800 dark:hover:text-slate-200 transition-colors duration-300">GitHub</a>
        <a href="https://www.linkedin.com/in/joshcourtney402/" target="_blank" rel="noopener noreferrer" className="hover:underline hover:text-slate-800 dark:hover:text-slate-200 transition-colors duration-300">LinkedIn</a>
      </div>
    </footer>
  );
} 