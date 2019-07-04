import React from 'react'
import { Switch, Route } from 'react-router-dom'
import Customers from './Customers'
import Invoices from './Invoices'

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
  <div className='flex-container-col'>
    <div className='panel'>
      <h1>Comp250 front-end</h1>
    </div>
  </div>
)
