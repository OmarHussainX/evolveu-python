import React, { Component } from 'react'
import axios from 'axios'

const DEBUG_MSG = true

class DeleteCustomer extends Component {
  constructor(props) {
    super(props)

    this.state = {
      customer: {
        id: null,
        first_name: '',
        last_name: ''
      }
    }
  }

  componentDidMount = async () => {
    if (DEBUG_MSG) console.log(`--- DeleteCustomer componentDidMount`)
    const customer = (await axios.get(`http://127.0.0.1:5000/customers/${this.props.match.params.id}`)).data

    this.setState({
      customer: {
        id: customer.id,
        first_name: customer.first_name,
        last_name: customer.last_name
      }
    })
  }

  cancelForm = () => {
    this.props.history.push('/customers')
  }

  submitForm = async (event) => {
    const { customer } = this.state
    // event.preventDefault()        //prevent form submission
    if (!customer.id) return

    const response = await axios.delete(`http://127.0.0.1:5000/customers/${customer.id}`)

    if (DEBUG_MSG) {
      console.log(`--- response after deleting customer:\n`)
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
          <h1>Delete Customer</h1>
          <p>
            Delete <strong>{first_name} {last_name}</strong>? (Associated invoices will also be deleted.)
          </p>
          <button onClick={this.submitForm} className='severe'>Delete</button>
          <button onClick={this.cancelForm}>Cancel</button>
        </div>
      </div>
    )
  }
}

export default DeleteCustomer
