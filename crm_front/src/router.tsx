import ProtectedRoute from "./utils/ProtectedRoute";
import UsersCard from "./page/Card/UsersCard/UsersCard";
import Login from "./page/Login/Login";
import Users from "./page/Users/Users";
import Home from "./page/Home/Home";
import {
    createBrowserRouter,
    createRoutesFromElements,
    Route,
} from "react-router-dom";
import App from "./App";
import Employees from "./page/Employees/Employees";
import NotFound from "./page/NotFound/NotFound";
import EmployeeCard from "./page/Card/EmpCard/EmployeeCard";
import Positions from "./page/Positions/Positions";


const router = createBrowserRouter(
    createRoutesFromElements(
        <>
            <Route path='/login' element={<Login />} />
            <Route path="/" element={<ProtectedRoute><App /></ProtectedRoute>}>
                <Route index element={<Home />} />
                <Route path="users" element={<Users />} />
                <Route path="users/:id" element={<UsersCard />} />
                <Route path="employees" element={<Employees />} />
                <Route path="employees/:id" element={<EmployeeCard />} />
                <Route path="positions" element={<Positions />} />
            </Route>
            <Route path="*" element={<NotFound />} />
        </>
    )
);


export default router;