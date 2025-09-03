import { formatDateString } from "../../utils/utils";
import styles from "./ContentItem.module.css";
import { Link } from "react-router-dom";

interface IContentItemProps {
  id: number;
  title: string;
  endpoint?: string;
  createdAt: string;
  onClick?: () => void;
}

function ContentItem({ id, title, endpoint, createdAt, onClick }: IContentItemProps) {
  const formattedDate = formatDateString(createdAt);

  return (
    <div className={styles["content-item"]} id={id.toString()}>
      <div>
        <p className="text-md font-bold">{title}</p>
        <span className="text-xs">{formattedDate}</span>
      </div>
      <div className="flex gap-2.5 justify-center items-center">
        {endpoint ? (
          <>
            <Link
              to={`/${endpoint}/${id}`}
              className="cursor-pointer hover:opacity-50"
            >
              🛠️
            </Link>
            <Link
              to={`/${endpoint}/${id}`}
              className="cursor-pointer hover:opacity-50"
            >
              ❌
            </Link>
          </>
        ) :
          (
            <div className="cursor-pointer hover:opacity-50"
              onClick={onClick}>
              ❌
            </div>
          )
        }
      </div>
    </div>
  );
}

export default ContentItem;
