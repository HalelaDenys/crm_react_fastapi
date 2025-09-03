import { Link } from "react-router-dom";
import styles from "../Page.module.css";

function NotFound() {
  return (
    <div className="flex flex-col gap-2 bg-[#d79c42]  min-h-screen">
      <h1 className="text-center font-medium text-3xl mt-4 italic">
        Нажаль нічого не знайдено !
      </h1>
      <img
        src="/not_found_image.png"
        alt="404"
        className="w-[600px] h-[600px] mx-auto"
      />
      <button className={` ${styles["btn"]} mx-auto w-[400px]`}>
        <Link to="/">Повернутися на головну</Link>
      </button>
    </div>
  );
}

export default NotFound;
