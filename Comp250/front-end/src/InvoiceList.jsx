import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

const DEBUG_MSG = true

class InvoiceList extends Component {
  constructor(props) {
    if (DEBUG_MSG) console.log(`--- InvoiceList constructor`)
    super(props)

    this.state = {
      invoices: null
    }
  }

  componentDidMount = async () => {
    if (DEBUG_MSG) console.log(`--- InvoiceList componentDidMount`)
    const invoices = (await axios.get('http://127.0.0.1:5000/invoices')).data
    this.setState({
      invoices,
    })
  }

  
  render() {
    return (
      <div className='flex-container-col'>
        <div className='panel'>
          <h1>Invoices</h1>
          <table className='invoices'>
            <thead>
              <tr>
                <th>id #</th>
                <th>Cust. id</th>
                <th>&nbsp;Date</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {this.state.invoices === null ? (
                <tr>
                  <td colSpan={4}>No data...</td>
                </tr>
              ) : (
                  this.state.invoices.map(inv => (
                    <tr key={inv.id}>
                      <td><em>{inv.id}</em></td>
                      <td>{inv.customer_id}</td>
                      <td>&nbsp;{inv.date}</td>
                      <td>
                        <Link
                          className='button-link'
                          to={`/invoices/details/${inv.id}`}>
                          View details
                        </Link>
                      </td>
                    </tr>
                  ))
                )}
            </tbody>
          </table>
        </div>
      </div>
    )
  }
}

export default InvoiceList
