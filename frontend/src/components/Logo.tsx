import React from 'react';

export default function Logo() {
  return (
    <div className="flex items-center gap-2">
      <img src="/globe.svg" alt="Data Ghost Logo" className="h-8 w-8" />
      <span className="text-2xl font-bold tracking-tight">Data Ghost</span>
    </div>
  );
} 