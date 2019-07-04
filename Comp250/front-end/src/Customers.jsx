import React, { Component } from 'react'
import axios from 'axios'

const DEBUG_MSG = true  // control output of debug messages

class Customers extends Component {
  constructor(props) {
    if (DEBUG_MSG) console.log(`--- Customers constructor`)
    super(props)

    this.state = {
      customers: null,
    }
  }

  async componentDidMount() {
    if (DEBUG_MSG) console.log(`--- Customers componentDidMount`)
    const customers = (await axios.get('http://127.0.0.1:5000/customers')).data
    this.setState({
      customers,
    })
  }

  render() {
    return (
      <div className='flex-container-col'>
        <div className='panel'>
          <h1>Customers</h1>
          <button className='prominent'>Add customer</button>
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
                  <td colSpan={3}>No users</td>
                </tr>
              ) : (
                  this.state.customers.map(cust => (
                    <tr key={cust.id}>
                      <td><em>{cust.id}</em></td>
                      <td>{cust.first_name} {cust.last_name}</td>
                      <td>
                        <button>Edit</button>
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
