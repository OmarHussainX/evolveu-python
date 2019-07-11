import React from 'react'
import { Switch, Route } from 'react-router-dom'
import InvoiceList from './InvoiceList'
import InvoiceDetails from './InvoiceDetails'


const Invoices = () => (
  <React.Fragment>
    <Switch>
      <Route exact path='/invoices' component={InvoiceList} />
      <Route path='/invoices/details/:id' component={InvoiceDetails} />
    </Switch>
  </React.Fragment>
)

export default Invoices
