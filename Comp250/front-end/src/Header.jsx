import React from 'react'
import { NavLink } from 'react-router-dom'

const Header = () => (
  <header>
    <nav>
      <ul>
        <li><NavLink to='/'>Home</NavLink></li>
        <li><NavLink to='/customers'>Customers</NavLink></li>
        <li><NavLink to='/invoices'>Invoices</NavLink></li>
      </ul>
    </nav>
  </header>
)

export default Header
