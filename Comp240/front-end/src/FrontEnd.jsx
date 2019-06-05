import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './FrontEnd.css'

const DEBUG_MSG = true  // control output of debug messages


const FrontEnd = () => {
  if (DEBUG_MSG) console.log(`--- FrontEnd()`)

  const [data, setData] = useState([])

  // Akin to componentDidMount, componentDidUpdate, componentWillUnmount combined.
  // Runs after every render: both after the first render and after every update,
  // unless customised otherwise.
  // New function is created after every render - each effect “belongs” to a
  // particular render.
  // 
  // Data Fetching with React Hooks
  // https://www.robinwieruch.de/react-hooks-fetch-data/
  useEffect(() => {
    if (DEBUG_MSG) console.log(`--- useEffect()`)

    const fetchData = async () => {
      if (DEBUG_MSG) console.log(`--- fetchData()`)
      const result = await axios(
        'http://127.0.0.1:5000/datadump',
      )

      setData(result.data)
      if (DEBUG_MSG) console.log(`--- result: ${result}\n
      keys: ${Object.keys(result)}\n
      values: ${Object.values(result)}`)
      if (DEBUG_MSG) console.log(`--- result.data: ${result.data}\ntype: ${typeof result.data}`)
    }

    fetchData()
  }, [])

  return (
    <div className="flex-container-col">
      <div className="panel">
        <header>
          <h2>Data from Flask server's <code>'/datadump'</code> route</h2>
        </header>
        <div className="cardsContainer">
          <div className="card">

            <table>
              <thead>
                <tr>
                  <td>Customer ID</td>
                  <td>Name</td>
                </tr>
              </thead>
              <tbody>
                {/* When no data is avaialable, map() will return an emtpy array */}
                {data.map(item => (
                  <tr key={item.Customer}>
                    <td>{item.Customer}</td>
                    <td>{item.First} {item.Last}</td>
                  </tr>
                ))}
              </tbody>
            </table>

          </div>
        </div>
      </div>
    </div>
  )
}

export default FrontEnd
