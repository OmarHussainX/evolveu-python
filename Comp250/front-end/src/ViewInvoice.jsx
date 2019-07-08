import React, { Component } from 'react'
import axios from 'axios'

const DEBUG_MSG = true

class ViewInvoice extends Component {
  constructor(props) {
    super(props)

    this.state = {
      invoice: null
    }
  }

  componentDidMount = async () => {
    if (DEBUG_MSG) console.log(`--- ViewInvoice componentDidMount`)
    const invoice = (await axios.get(`http://127.0.0.1:5000/invoicedetails/${this.props.location.state.id}`)).data

    if (DEBUG_MSG) {
      console.log(`--- details of invoice:\n`)
      for (let [key, value] of Object.entries(invoice)) {
        console.log(`${key}: ${value}`)
      }
    }

      this.setState({
        invoice,
      })
    }

    goBack = () => {
      this.props.history.push('/invoices')
    }


    render() {
      // const { first_name, last_name } = this.state.customer
      return (
        <div className='flex-container-col'>
          <div className='panel'>
            <h1>Invoice # {this.props.location.state.id}</h1>
            <p>
              <em>invoice details go here...</em>
            </p>
            <button onClick={this.goBack}>Back</button>
          </div>
        </div>
      )
    }
  }

  export default ViewInvoice
