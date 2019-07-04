import React, { Component } from 'react'
import axios from 'axios'

const DEBUG_MSG = true

class AddCustomer extends Component {
    constructor(props) {
        if (DEBUG_MSG) console.log(`--- AddCustomer constructor`)
        super(props)

        this.state = {
            customer: {
                first_name: 'first',
                last_name: 'last'
            },
        }
    }

    componentDidMount = () => {
        if (DEBUG_MSG) console.log(`--- AddCustomer componentDidMount`)
    }

    handleChange = event => {
        const { name, value } = event.target
        if (DEBUG_MSG) console.log(`--- AddCustomer handleChange`)
        if (DEBUG_MSG) console.log(`name: ${name}, value: ${value}`)

        this.setState((prevState) => ({
            customer: { ...prevState.customer, [name]: value }
        }))
    }

    render() {
        const { first_name, last_name } = this.state.customer
        return (
            <div className='flex-container-col'>
                <div className='panel'>
                    <h1>Add Customer</h1>
                    <form>
                        <fieldset>
                            <legend>Name</legend>
                            <input type="text" name="firstname" value={first_name} onChange={this.handleChange} />
                            <input type="text" name="lastname" value={last_name} onChange={this.handleChange} />
                        </fieldset>
                        <button>Submit</button>
                        <button>Cancel</button>
                    </form>
                </div>
            </div>
        )
    }
}

export default AddCustomer
