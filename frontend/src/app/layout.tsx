import '@/styles/globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Filmmaker - AI Video Generator',
  description: 'Create stunning videos from text with AI',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen flex flex-col">
          <header className="py-6 bg-white shadow-sm">
            <div className="container mx-auto px-4">
              <h1 className="text-2xl font-semibold">Filmmaker</h1>
            </div>
          </header>
          <main className="flex-grow container mx-auto px-4 py-8">
            {children}
          </main>
          <footer className="py-6 bg-secondary">
            <div className="container mx-auto px-4 text-center text-gray-500 text-sm">
              © {new Date().getFullYear()} Filmmaker. All rights reserved.
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
} 