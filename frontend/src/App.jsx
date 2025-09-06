import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import Portfolio from './pages/Portfolio.jsx'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('home')

  const renderPage = () => {
    switch(currentPage) {
      case 'portfolio':
        return <Portfolio />
      default:
        return (
          <div className="min-h-screen bg-black text-white">
            <div className="container mx-auto px-4 py-8">
              <header className="text-center mb-12">
                <div className="mb-8">
                  <img 
                    src="/assets/logo.png" 
                    alt="Fifth Element Photography Logo" 
                    className="mx-auto w-48 h-48 md:w-64 md:h-64 object-contain"
                  />
                </div>
                <h1 className="text-3xl md:text-5xl font-bold mb-4 tracking-wider">
                  FIFTH ELEMENT PHOTOGRAPHY
                </h1>
                <p className="text-lg md:text-xl text-gray-300 italic">
                  Capturing the Quintessence
                </p>
              </header>
              
              <main className="text-center">
                <div className="mb-8">
                  <h2 className="text-xl md:text-2xl mb-4">Welcome to our artistic photography portfolio</h2>
                  <p className="text-gray-400 mb-6 max-w-2xl mx-auto">
                    Experience the art of photography through our lens. Each image captures the essential 
                    beauty and emotion of the moment - the quintessence of visual storytelling.
                  </p>
                </div>
                
                <div className="space-y-4">
                  <Button 
                    onClick={() => setCurrentPage('portfolio')}
                    className="bg-white text-black hover:bg-gray-200 px-8 py-3 text-lg"
                  >
                    View Portfolio
                  </Button>
                  <br />
                  <Button 
                    variant="outline" 
                    className="border-white text-white hover:bg-white hover:text-black px-8 py-3 text-lg"
                  >
                    About Us
                  </Button>
                </div>
              </main>
              
              <footer className="text-center mt-16 text-gray-500">
                <p>Professional photography with artistic vision and technical excellence</p>
              </footer>
            </div>
          </div>
        )
    }
  }

  return renderPage()
}

export default App

