import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import Game from './Game'
import Start from './Start'

function App() {

  return (

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Start />} />
          <Route path="/game" element={<Game />} />
        </Routes>
      </BrowserRouter>
    
  )
}

export default App
