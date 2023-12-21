import React, { Suspense } from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import {
  Outlet,
  RouterProvider,
  Router,
  Route,
  RootRoute,
} from '@tanstack/react-router'

const Register = React.lazy(() => import('./routes/Register'))

const rootRoute = new RootRoute({
    component: () => (
        <>
            <Outlet />
        </>
    ),
})

const registerRoute = new Route({
    getParentRoute: () => rootRoute,
    path: "/register",
    component: () => <Suspense><Register /></Suspense>
})

const routeTree = rootRoute.addChildren([registerRoute])

const router = new Router({ routeTree })

declare module '@tanstack/react-router' {
    interface Register {
        router: typeof router
    }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <RouterProvider router={router} />
    </React.StrictMode>,
)
