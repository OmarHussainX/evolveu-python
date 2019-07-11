import React from 'react'
import { Switch, Route } from 'react-router-dom'
import Customers from './Customers'
import AddCustomer from './forms/AddCustomer'
import EditCustomer from './forms/EditCustomer'
import DeleteCustomer from './forms/DeleteCustomer'
import Invoices from './Invoices'
import ViewInvoice from './ViewInvoice'

const Main = () => {
  return (
    <main>
      <Switch>
        <Route exact path='/' component={Home} />
        <Route path='/customers' component={Customers} />
        <Route path='/addcustomer' component={AddCustomer} />
        <Route path='/editcustomer' component={EditCustomer} />
        <Route path='/deletecustomer' component={DeleteCustomer} />
        <Route path='/invoices' component={Invoices} />
        <Route path='/viewinvoice/:id' component={ViewInvoice} />
      </Switch>
    </main>
  )
}
export default Main

const Home = () => (
  <div className='flex-container-col'>
    <div className='panel'>
      <h1>Comp250 front-end</h1>
    </div>
  </div>
)
