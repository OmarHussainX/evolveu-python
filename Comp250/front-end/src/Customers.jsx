import React from 'react'
import { Switch, Route } from 'react-router-dom'
import CustomerList from './CustomerList'
import AddCustomer from './forms/AddCustomer'
import EditCustomer from './forms/EditCustomer'
import DeleteCustomer from './forms/DeleteCustomer'


const Customers = () => (
    <Switch>
      <Route exact path='/customers' component={CustomerList} />
      <Route path='/customers/add' component={AddCustomer} />
      <Route path='/customers/edit/:id' component={EditCustomer} />
      <Route path='/customers/delete/:id' component={DeleteCustomer} />
    </Switch>
)

export default Customers
