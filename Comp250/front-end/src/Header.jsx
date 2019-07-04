import React from 'react'
import { NavLink } from 'react-router-dom'

const Header = () => (
  <header>
    <nav>
      <div className='flex-container-col'>
        <div className='panel'>
          <ul>
            <li>
              <NavLink exact
                activeClassName='active'
                to='/'>
                Home
              </NavLink>
            </li>
            <li>
              <NavLink
                activeClassName='active'
                to='/customers'>
                List customers
              </NavLink>
            </li>
            <li>
              <NavLink
                activeClassName='active'
                to='/invoices'>
                List invoices
              </NavLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
)

export default Header
