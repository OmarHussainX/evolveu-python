import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'


class Customers extends Component {
  constructor(props) {
    super(props)
    this.state = {
      customers: null,
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

  
  render() {
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
                        <Link
                          className='button-link'
                          to={`/editcustomer/${cust.id}`}>
                          Edit
                        </Link>
                        <Link
                          className='button-link'
                          to={`/deletecustomer/${cust.id}`}>
                          Delete
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

export default Customers
