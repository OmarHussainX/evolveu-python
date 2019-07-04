import React from 'react'
import { Switch, Route } from 'react-router-dom'

const Main = () => {
  return (
    <main>
      <Switch>
        <Route exact path='/' component={Home}/>
        <Route path='/customers' component={Customers}/>
        <Route path='/invoices' component={Invoices}/>
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

  const Customers = () => (
    <div>
      <h1>Customers</h1>
    </div>
  )

  const Invoices = () => (
    <div>
      <h1>Invoices</h1>
    </div>
  )
      