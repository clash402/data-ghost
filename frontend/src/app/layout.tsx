import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import ThemeProvider from "@/components/ThemeProvider";

const geist = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Data Ghost - CSV Data Analysis",
  description: "Upload your CSV data and ask questions about it with AI-powered analysis",
  keywords: ["CSV", "data analysis", "AI", "query", "spreadsheet"],
  authors: [{ name: "Data Ghost Team" }],
  icons: {
    icon: "/favicon.png",
  },
  openGraph: {
    title: "Data Ghost - CSV Data Analysis",
    description: "Upload your CSV data and ask questions about it with AI-powered analysis",
    type: "website",
    images: [
      {
        url: "/share-image.png",
        width: 1200,
        height: 630,
        alt: "Data Ghost - AI-powered CSV data analysis",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Data Ghost - CSV Data Analysis",
    description: "Upload your CSV data and ask questions about it with AI-powered analysis",
    images: ["/share-image.png"],
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geist.variable} ${geistMono.variable} antialiased`}
      >
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
