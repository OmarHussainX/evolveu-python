import React, { Component } from 'react'
import axios from 'axios'

class Customers extends Component {
  constructor(props) {
    super(props)

    this.state = {
      customers: null,
    }
  }

  async componentDidMount() {
    const customers = (await axios.get('http://127.0.0.1:5000/customers')).data
    console.log(`customers: ${customers}`)
    this.setState({
      customers,
    })
  }

  render() {
    return (
      <div>
        <h1>List of customers</h1>
        <table>
          <thead>
            <tr>
              <th>First</th>
              <th>Last</th>
              <th>Actions</th>
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
                    <td>{cust.first_name}</td>
                    <td>{cust.last_name}</td>
                    <td>
                      <button>Edit</button>
                      <button>Delete</button>
                    </td>
                  </tr>
                ))
              )}
          </tbody>
        </table>
      </div>
    )
  }
}
export default Customers
