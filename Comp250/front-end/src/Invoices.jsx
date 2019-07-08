import React, { Component } from 'react'
import { Redirect } from 'react-router'
import axios from 'axios'

const DEBUG_MSG = true

class Invoices extends Component {
  constructor(props) {
    if (DEBUG_MSG) console.log(`--- Invoices constructor`)
    super(props)

    this.state = {
      invoices: null,
      viewInvoice: false,
      invoice_id: null
    }
  }

  componentDidMount = async () => {
    if (DEBUG_MSG) console.log(`--- Invoices componentDidMount`)
    const invoices = (await axios.get('http://127.0.0.1:5000/invoices')).data
    this.setState({
      invoices,
    })
  }

  viewInvoice = event => {
    this.setState({
      viewInvoice: true,
      invoice_id: event.target.id.slice('viewInv_'.length)
    })
  }

  
  render() {
    if (this.state.viewInvoice) {
        return <Redirect
          to={{
            pathname: '/viewinvoice',
            state: { id: this.state.invoice_id }
          }}
        />
      } else return (
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
                        <button id={'viewInv_' + inv.id} onClick={this.viewInvoice}>View details</button>
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

export default Invoices
