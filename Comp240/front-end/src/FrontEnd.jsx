import React, { useState } from 'react'
import './FrontEnd.css'

const FrontEnd = () => {
  return (
    <div class="flex-container-col">
      <div class="panel">
        <header>
          <h2>Data from Flask server's <code>'/viewdata'</code> route</h2>
        </header>
        <div class="cardsContainer">
          <div class="card">
            <p>
              Initial setup of front end to communicate with Flask server
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FrontEnd
