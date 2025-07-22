import React from 'react';
import { Ghost } from 'lucide-react';

export default function Logo() {
  return (
    <div className="flex items-center gap-2 sm:gap-3 px-3 py-2">
      <Ghost 
        className="h-6 w-6 sm:h-8 sm:w-8 drop-shadow transition-all duration-300 text-slate-700 dark:text-slate-300"
      />
      <span className="text-xl sm:text-2xl lg:text-3xl font-bold tracking-tight text-slate-800 dark:text-slate-100 transition-colors duration-300">
        Data Ghost
      </span>
    </div>
  );
} 