import React, { Component } from 'react'
import axios from 'axios'

const DEBUG_MSG = true

class AddCustomer extends Component {
  constructor(props) {
    if (DEBUG_MSG) console.log(`--- AddCustomer constructor`)
    super(props)

    this.state = {
      customer: {
        first_name: '',
        last_name: ''
      },
    }
  }

  handleChange = event => {
    const { name, value } = event.target
    if (DEBUG_MSG) console.log(`--- AddCustomer handleChange`)
    if (DEBUG_MSG) console.log(`name: ${name}, value: ${value}`)

    this.setState((prevState) => ({
      customer: { ...this.state.customer, [name]: value }
    }))
  }

  cancelForm = () => {
    this.props.history.push('/customers')
  }

  submitForm = async (event) => {
    event.preventDefault()  //prevent form submission
    if (DEBUG_MSG) console.log(`--- AddCustomer submitForm`)

    const response = await axios.post('http://127.0.0.1:5000/customers', this.state.customer)

    if (DEBUG_MSG) {
      console.log(`--- response after adding customer:\n`)
      for (let [key, value] of Object.entries(response)) {
        console.log(`${key}: ${value}`)
      }
    }

    this.props.history.push('/customers')
  }

  render() {
    const { first_name, last_name } = this.state.customer
    return (
      <div className='flex-container-col'>
        <div className='panel'>
          <h1>Add Customer</h1>
          <form>
            <input
              type='text'
              name='first_name'
              placeholder='Enter first name'
              value={first_name}
              onChange={this.handleChange} />
            <input
              type='text'
              name='last_name'
              placeholder='Enter last name'
              value={last_name}
              onChange={this.handleChange} />
            <br />
            <button onClick={this.submitForm}>Submit</button>
            <button onClick={this.cancelForm}>Cancel</button>
          </form>
        </div>
      </div>
    )
  }
}

export default AddCustomer
