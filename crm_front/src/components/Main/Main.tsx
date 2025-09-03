import { Outlet } from "react-router-dom";

function Main() {
    return (
        <main className="flex-1 p-6 bg-gray-400">
            <h1 className="text-center font-bold text-3xl">SRM</h1>
            {/* {showFilter && <FilterItem />} */}
            <div className="container px-2">
                <Outlet />
            </div>
        </main>
    );
}

export default Main;