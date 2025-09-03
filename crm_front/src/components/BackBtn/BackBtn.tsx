import { Link } from "react-router-dom";


interface BackBtnProps {
    endpoint: string;
}

export default function BackBtn({ endpoint }: BackBtnProps) {
    return (
        <Link
            to={`/${endpoint}`}
            className="cursor-pointer hover:opacity-50 flex items-center gap-1 text-xl font-bold"
        >
            <img src="/arrow-left.svg" alt="Back" className="w-5 h-5" /> Back
        </Link>
    );
}
