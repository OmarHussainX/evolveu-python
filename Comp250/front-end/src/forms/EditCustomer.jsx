import React, { Component } from 'react'
import axios from 'axios'

const DEBUG_MSG = true

class EditCustomer extends Component {
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
    if (DEBUG_MSG) console.log(`--- EditCustomer componentDidMount`)
    const customer = (await axios.get(`http://127.0.0.1:5000/customers/${this.props.match.params.id}`)).data

    this.setState({
      customer: {
        id: customer.id,
        first_name: customer.first_name,
        last_name: customer.last_name
      }
    })
  }

  handleChange = event => {
    const { name, value } = event.target
    this.setState((prevState) => ({
      customer: { ...prevState.customer, [name]: value }
    }))
  }

  cancelForm = (event) => {
    event.preventDefault()        //prevent form submission
    this.props.history.push('/customers')
  }

  submitForm = async (event) => {
    const { customer } = this.state
    event.preventDefault()        //prevent form submission
    if (!customer.first_name || !customer.last_name) return

    const response = await axios.patch('http://127.0.0.1:5000/customers', customer)

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
          <h1>Edit Customer</h1>
          <form>
            <input
              type='text'
              name='first_name'
              value={first_name}
              onChange={this.handleChange} />
            <input
              type='text'
              name='last_name'
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

export default EditCustomer
