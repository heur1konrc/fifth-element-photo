import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import './App.css'

function App() {
  return (
    <div className="min-h-screen bg-black text-white">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">
            Fifth Element Photography
          </h1>
          <p className="text-xl md:text-2xl text-gray-300">
            Capturing the Quintessence
          </p>
        </header>
        
        <main className="text-center">
          <div className="mb-8">
            <h2 className="text-2xl mb-4">Welcome to our artistic photography portfolio</h2>
            <p className="text-gray-400 mb-6">
              Your sophisticated, dark artistic photography website is being built.
            </p>
          </div>
          
          <div className="space-y-4">
            <Button className="bg-white text-black hover:bg-gray-200">
              View Portfolio
            </Button>
            <br />
            <Button variant="outline" className="border-white text-white hover:bg-white hover:text-black">
              About Us
            </Button>
          </div>
        </main>
        
        <footer className="text-center mt-16 text-gray-500">
          <p>Dark artistic theme designed for your black background logo</p>
        </footer>
      </div>
    </div>
  )
}

export default App

