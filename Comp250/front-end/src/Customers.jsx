import React, { Component } from 'react'
import { Redirect } from 'react-router'
import axios from 'axios'


class Customers extends Component {
  constructor(props) {
    super(props)
    this.state = {
      customers: null,
      editCustomer: false,
      customer_id: null
    }
  }

  componentDidMount = async () => {
    const customers = (await axios.get('http://127.0.0.1:5000/customers')).data
    this.setState({
      customers,
    })
  }

  addCustomer = () => {
    this.props.history.push('/addcustomer')
  }

  editCustomer = event => {
    this.setState({
      editCustomer: true,
      customer_id: event.target.id.slice(9)
    })
}

  render() {
    if (this.state.editCustomer) {
      return <Redirect
        to={{
          pathname: '/editcustomer',
          state: { id: this.state.customer_id }
        }}
      />
    }
    return (
      <div className='flex-container-col'>
        <div className='panel'>
          <h1>Customers</h1>
          <button
            className='prominent'
            onClick={this.addCustomer}>
            Add customer
            </button>
          <table className='customers'>
            <thead>
              <tr>
                <th>id #</th>
                <th>Name</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {this.state.customers === null ? (
                <tr>
                  <td colSpan={3}>No data...</td>
                </tr>
              ) : (
                  this.state.customers.map(cust => (
                    <tr key={cust.id}>
                      <td><em>{cust.id}</em></td>
                      <td>{cust.first_name} {cust.last_name}</td>
                      <td>
                        <button id={'editCust_'+cust.id} onClick={this.editCustomer}>Edit</button>
                        <button>Delete</button>
                        {/* <button className='severe'>Delete</button> */}
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

export default Customers
