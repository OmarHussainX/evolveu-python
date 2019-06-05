import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './FrontEnd.css'


// Set to 'true' to enable output of debug messages
const DEBUG_MSG = true

const FrontEnd = () => {
  if (DEBUG_MSG) console.log(`--- FrontEnd()`)

  const [data, setData] = useState({ hits: [] })

  // Akin to componentDidMount, componentDidUpdate, and componentWillUnmount combined
  // Runs after every render: both after the first render and after every update,
  // unless customised otherwise
  // New function is created after every render - each effect “belongs” to a
  // particular render
  useEffect(() => {
    if (DEBUG_MSG) console.log(`--- useEffect()`)
    const fetchData = async () => {
      const result = await axios(
        // 'http://hn.algolia.com/api/v1/search?query=redux',
        'http://127.0.0.1:5000/datadump',
      )

      setData(result.data)
    }

    fetchData()
  }, [])
  return (
    <div class="flex-container-col">
      <div class="panel">
        <header>
          <h2>Data from Flask server's <code>'/datadump'</code> route</h2>
        </header>
        <div class="cardsContainer">
          <div class="card">
            <p>
              {/* {excelData.length ? excelData : 'No data loaded...'} */}
            </p>
            <ul>
              {data.hits.map(item => (
                <li key={item.objectID}>
                  <a href={item.url}>{item.title}</a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FrontEnd
