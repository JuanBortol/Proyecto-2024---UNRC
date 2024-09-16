import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import AppRouter from './Router.jsx'
import './styles/index.css'
import { AppProvider } from './components/AppContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AppProvider>
      <AppRouter />
    </AppProvider>
  </StrictMode>,
)
