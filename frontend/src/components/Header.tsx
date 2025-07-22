import React from 'react';
import Logo from './Logo';
import DarkModeToggle from './DarkModeToggle';

export default function Header() {
  return (
    <header className="w-full flex items-center justify-between px-4 sm:px-6 lg:px-8 py-4 sm:py-6 ghost-header glass-card">
      <Logo />
      <DarkModeToggle />
    </header>
  );
} 