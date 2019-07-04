import React from 'react'
import { Switch, Route } from 'react-router-dom'
import Customers from './Customers'

const Main = () => {
  return (
    <main>
      <Switch>
        <Route exact path='/' component={Home} />
        <Route path='/customers' component={Customers} />
        <Route path='/invoices' component={Invoices} />
      </Switch>
    </main>
  )
}
export default Main

const Home = () => (
  <div>
    <h1>Comp250 front-end</h1>
  </div>
)

const Invoices = () => (
  <div>
    <h1>List of invoices</h1>
  </div>
)
