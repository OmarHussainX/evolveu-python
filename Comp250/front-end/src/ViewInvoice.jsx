import React, { Component } from 'react'
import axios from 'axios'

const DEBUG_MSG = true

class ViewInvoice extends Component {
  constructor(props) {
    super(props)

    this.state = {
      inv_data: null
    }
  }

  componentDidMount = async () => {
    if (DEBUG_MSG) console.log(`--- ViewInvoice componentDidMount`)
    const inv_data = (await axios.get(`http://127.0.0.1:5000/invoicedetails/${this.props.location.state.id}`)).data

    if (DEBUG_MSG) {
      console.log(`--- details of invoice:\n`)
      for (let [key, value] of Object.entries(inv_data)) {
        console.log(`${key}: ${value}`)
      }
    }

    this.setState({
      inv_data,
    })
  }

  goBack = () => {
    this.props.history.push('/invoices')
  }


  render() {
    const { inv_data } = this.state
    if (inv_data === null) {
      return (
        <div>No data...</div>
      )
    } else return (
      <div className='flex-container-col'>
        <div className='panel'>
          <h1>
            Invoice # {this.props.location.state.id}
            <span>{inv_data.date}</span></h1>
          <p className='invoice-customer'>
            {inv_data.customer.first_name} {inv_data.customer.last_name}
            &nbsp;<span>(customer id: {inv_data.customer.id})</span>
          </p>
          <table className='invoice-details'>
            <thead>
              <tr>
                <th className='units'>Quantity</th>
                <th className='item'>Item</th>
                <th>Unit price</th>
                <th></th>
                <th>Line total</th>
              </tr>
            </thead>
            <tbody>
              {inv_data.line_items.map(item => (
                <tr key={item.id}>
                  <td className='units'>{item.units}</td>
                  <td className='item'>{item.product}</td>
                  <td className='price'>${item.price}</td>
                  <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
                  <td className='price'>${item.line_total}</td>
                </tr>
              ))}
            </tbody>
            <tfoot>
              <tr>
                <td colSpan={4}>TOTAL</td>
                <td className='price'>${inv_data.total}</td>
              </tr>
            </tfoot>
          </table>
          <button onClick={this.goBack}>Back</button>
        </div>
      </div>
    )
  }
}

export default ViewInvoice
