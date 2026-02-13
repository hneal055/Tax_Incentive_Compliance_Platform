/**
 * PilotForge - Tax Incentive Intelligence for Film & TV
 * Copyright (c) 2026 PilotForge - Tax Incentive Compliance Platform
 * All Rights Reserved.
 * 
 * PROPRIETARY AND CONFIDENTIAL
 * This software is proprietary and confidential. Unauthorized copying,
 * distribution, modification, or use is strictly prohibited.
 */
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
