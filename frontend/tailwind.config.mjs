import defaultTheme from 'tailwindcss/defaultTheme';

const config = {
  darkMode: 'class',
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './src/app/**/*.{js,ts,jsx,tsx}',
    './src/components/**/*.{js,ts,jsx,tsx}',
    './src/pages/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        ghost: {
          50:  '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        'glass-white': 'rgba(255,255,255,0.6)',
        'glass-dark': 'rgba(30,41,59,0.6)',
      },
      backgroundImage: {
        'ghost-gradient': 'linear-gradient(135deg, #f1f5f9 0%, #64748b 100%)',
        'ghost-gradient-dark': 'linear-gradient(135deg, #1e293b 0%, #334155 100%)',
      },
      boxShadow: {
        ghost: '0 4px 32px 0 rgba(100,116,139,0.12)',
        glass: '0 8px 32px 0 rgba(31,41,55,0.18)',
      },
      borderRadius: {
        xl: '1.25rem',
      },
      backdropBlur: {
        xs: '2px',
        sm: '4px',
        md: '8px',
        lg: '16px',
      },
      transitionProperty: {
        'colors': 'background-color, border-color, color, fill, stroke',
        'spacing': 'margin, padding',
      },
    },
    fontFamily: {
      sans: [
        'var(--font-geist-sans)',
        ...defaultTheme.fontFamily.sans,
      ],
      mono: [
        'var(--font-geist-mono)',
        ...defaultTheme.fontFamily.mono,
      ],
    },
  },
  plugins: [],
};

export default config; 