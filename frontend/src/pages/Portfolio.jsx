import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'

function Portfolio() {
  const [images, setImages] = useState([])
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch categories
  useEffect(() => {
    fetch('/api/categories')
      .then(res => res.json())
      .then(data => {
        setCategories(data)
      })
      .catch(err => {
        console.error('Error fetching categories:', err)
        setError('Failed to load categories')
      })
  }, [])

  // Fetch portfolio images
  useEffect(() => {
    setLoading(true)
    const params = new URLSearchParams({
      page: currentPage,
      per_page: 12
    })
    
    if (selectedCategory) {
      params.append('category_id', selectedCategory)
    }

    fetch(`/api/portfolio?${params}`)
      .then(res => res.json())
      .then(data => {
        setImages(data.images || [])
        setTotalPages(data.pages || 1)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching portfolio:', err)
        setError('Failed to load portfolio images')
        setLoading(false)
      })
  }, [selectedCategory, currentPage])

  const handleCategoryChange = (categoryId) => {
    setSelectedCategory(categoryId)
    setCurrentPage(1)
  }

  const handlePageChange = (page) => {
    setCurrentPage(page)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  if (error) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl mb-4">Error Loading Portfolio</h2>
          <p className="text-gray-400">{error}</p>
          <Button 
            onClick={() => window.location.reload()} 
            className="mt-4 bg-white text-black hover:bg-gray-200"
          >
            Retry
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold mb-4 tracking-wider">
            PORTFOLIO
          </h1>
          <p className="text-lg md:text-xl text-gray-300">
            Capturing the Quintessence
          </p>
        </header>

        {/* Category Filter */}
        <div className="mb-8">
          <div className="flex flex-wrap justify-center gap-4">
            <Button
              onClick={() => handleCategoryChange(null)}
              variant={selectedCategory === null ? "default" : "outline"}
              className={selectedCategory === null 
                ? "bg-white text-black hover:bg-gray-200" 
                : "border-white text-white hover:bg-white hover:text-black"
              }
            >
              All
            </Button>
            {categories.map(category => (
              <Button
                key={category.id}
                onClick={() => handleCategoryChange(category.id)}
                variant={selectedCategory === category.id ? "default" : "outline"}
                className={selectedCategory === category.id 
                  ? "bg-white text-black hover:bg-gray-200" 
                  : "border-white text-white hover:bg-white hover:text-black"
                }
              >
                {category.name}
              </Button>
            ))}
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
            <p className="mt-4 text-gray-400">Loading portfolio...</p>
          </div>
        )}

        {/* Portfolio Grid */}
        {!loading && (
          <>
            {images.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
                {images.map(image => (
                  <div 
                    key={image.id} 
                    className="group relative overflow-hidden rounded-lg bg-gray-900 aspect-square cursor-pointer hover:scale-105 transition-transform duration-300"
                  >
                    <img
                      src={image.web_path}
                      alt={image.alt_text || image.title || image.filename}
                      className="w-full h-full object-cover opacity-100"
                      loading="lazy"
                      style={{ display: 'block', visibility: 'visible' }}
                    />
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all duration-300 flex items-center justify-center">
                      <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-center p-4">
                        {image.title && (
                          <h3 className="text-white font-semibold mb-2">{image.title}</h3>
                        )}
                        {image.category_name && (
                          <span className="inline-block bg-white text-black px-3 py-1 rounded-full text-sm">
                            {image.category_name}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <h3 className="text-2xl mb-4">No Images Found</h3>
                <p className="text-gray-400 mb-6">
                  {selectedCategory 
                    ? `No images in the selected category yet.`
                    : `No images have been uploaded to the portfolio yet.`
                  }
                </p>
                {selectedCategory && (
                  <Button 
                    onClick={() => handleCategoryChange(null)}
                    className="bg-white text-black hover:bg-gray-200"
                  >
                    View All Categories
                  </Button>
                )}
              </div>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center space-x-4">
                <Button
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}
                  variant="outline"
                  className="border-white text-white hover:bg-white hover:text-black disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </Button>
                
                <span className="text-gray-300">
                  Page {currentPage} of {totalPages}
                </span>
                
                <Button
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  variant="outline"
                  className="border-white text-white hover:bg-white hover:text-black disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </Button>
              </div>
            )}
          </>
        )}

        {/* Back to Home */}
        <div className="text-center mt-12">
          <Button 
            onClick={() => window.location.href = '/'}
            variant="outline"
            className="border-white text-white hover:bg-white hover:text-black"
          >
            ← Back to Home
          </Button>
        </div>
      </div>
    </div>
  )
}

export default Portfolio

