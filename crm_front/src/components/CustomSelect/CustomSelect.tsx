import { useEffect, useRef, useState } from "react";

interface ICustomSelect {
  label: string;
  selectedValue?: number;
  options: { value: string; id: number }[];
  onChange?: (value: any) => void;
}

function CustomSelect({
  label,
  options,
  selectedValue,
  onChange,
}: ICustomSelect) {
  const ref = useRef<HTMLDivElement>(null);
  const [isOpen, setIsOpen] = useState(false);
  const selected =
    options.find((opt) => opt.id === selectedValue) || options[0];
  
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [ref]);

  return (
    <div className="flex flex-row gap-2 mx-1 items-center">
      <label className="text-lg font-medium italic">{label}</label>
      <div className="relative w-40" ref={ref}>
        <div
          onClick={() => setIsOpen(!isOpen)}
          className=" border p-2 rounded cursor-pointer"
        >
          <div className="flex justify-between items-center">
            {selected?.value}
                {
                  isOpen
                    ? <img src="/arrow-up.svg" alt="up icon" className="w-4 h-4 inline ml-2" />
                    : <img src="/arrow-down.svg" alt="down icon" className="w-4 h-4 inline ml-2" />
                }
          </div>
        </div>
        {isOpen && (
          <ul className="absolute top-full left-0 w-full 
          bg-gray-300 shadow-md z-10 border rounded">
            {options.map((option) => (
              <li
                key={option.id}
                onClick={() => {
                  {
                    onChange && onChange(option);
                  }
                  setIsOpen(false);
                }}
                className="p-2 hover:bg-gray-100 cursor-pointer"
              >
                {option.value}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default CustomSelect;
