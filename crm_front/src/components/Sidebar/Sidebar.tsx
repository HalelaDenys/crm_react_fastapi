import { NavLink } from "react-router-dom";
import styles from "./Sidebar.module.css";
import CustomSelect from "../CustomSelect/CustomSelect";
import { useState } from "react";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar = ({ isOpen, onClose }: SidebarProps) => {
  const [isOpen2, setIsOpen2] = useState(false);
  const options = [
    { value: "Посади", id: 2, endpoint: "/positions" },
  ]



  return (
    <nav
      className={`
                ${styles["Sidebar-wrapper"]}
                ${isOpen ? "translate-x-0 bg-gray-800/90" : "-translate-x-full"}
            `}
    >
      <button
        onClick={onClose}
        className={styles["closeSidebar"]}
        aria-label="Close sidebar"
      >
        X
      </button>
      <aside>
        <h2 className={styles["h2-style"]}>HOME</h2>
        <NavLink to="/users" className={styles["btn"]}>
          Користувачі
        </NavLink>
        <NavLink to="/employees" className={styles["btn"]}>
          Співробітники
        </NavLink>
        <NavLink to="/" className={styles["btn"]}>
          Користувачі
        </NavLink>


        <div className={styles["btn"]}>
          <div className="relative">
            <div
              onClick={() => setIsOpen2(!isOpen2)}
              className=" cursor-pointer"
            >

              <div className="flex justify-between items-center">
                Додаткове
                {
                  isOpen2
                    ? <img src="/arrow-up-white.svg" alt="up icon" className="w-4 h-4 inline ml-2" />
                    : <img src="/arrow-down-white.svg" alt="down icon" className="w-4 h-4 inline ml-2" />
                }
              </div>
            </div>
            {isOpen2 && (
              <ul
                className="mt-2 w-full"
              >
                {options.map((option) => (
                  <NavLink
                    to={option.endpoint} 
                    key={option.id}
                    // onClick={() => {
                    //   setTimeout(() => setIsOpen2(false), 100);
                    // }}
                    className="py-2 px-1 hover:text-red-600 cursor-pointer text-base block"
                  >
                    {option.value}
                  </NavLink>
                ))}
              </ul>
            )}
          </div>
        </div>
        <NavLink to="/" className={styles["btn"]}>
          Профіль
        </NavLink>

      </aside>
    </nav>
  );
};

export default Sidebar;
