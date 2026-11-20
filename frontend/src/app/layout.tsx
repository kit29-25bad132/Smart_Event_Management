import "./globals.css";
import type { Metadata } from "next";
export const metadata: Metadata = { title: "Smart Event Management", description: "Agentic AI Smart Event Management System" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
