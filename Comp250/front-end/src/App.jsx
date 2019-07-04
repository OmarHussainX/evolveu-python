import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import Header from './Header'
import Main from './Main'
import './App.css'

const App = () => {
  return (
    <BrowserRouter>
      <div>
        <Header />
        <Main />
      </div>
    </BrowserRouter>
  )
}

export default App
