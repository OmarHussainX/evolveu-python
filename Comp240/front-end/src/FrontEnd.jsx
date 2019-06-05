import React, { useState, useEffect } from 'react'
import './FrontEnd.css'


// Set to 'true' to enable output of debug messages
const DEBUG_MSG = true

const FrontEnd = () => {
    if (DEBUG_MSG) console.log(`--- FrontEnd()`)

    const [excelData, setExcelData] = useState([])

  // Akin to componentDidMount, componentDidUpdate, and componentWillUnmount combined
  // Runs after every render: both after the first render and after every update,
  // unless customised otherwise
  // New function is created after every render - each effect “belongs” to a
  // particular render
  useEffect(() => {
    if (DEBUG_MSG) console.log(`--- useEffect()`)
  })

  return (
    <div class="flex-container-col">
      <div class="panel">
        <header>
          <h2>Data from Flask server's <code>'/viewdata'</code> route</h2>
        </header>
        <div class="cardsContainer">
          <div class="card">
            <p>
              {excelData.length ? excelData : 'No data loaded...'}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FrontEnd
