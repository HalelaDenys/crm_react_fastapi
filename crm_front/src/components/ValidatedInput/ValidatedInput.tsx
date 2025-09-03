interface ValidatedInputProps {
  label: string;
  name: string;
  value?: string | number;
  type?: string;
  error?: string;
  onChange: (value: string) => void;
  checked?: boolean; // для checkbox
}

function ValidatedInput({
  label,
  name,
  value,
  type = "text",
  error,
  onChange,
  checked,
}: ValidatedInputProps) {
  return (
    <>
      <label className="text-lg font-medium italic mx-1">{label}</label>
      {type === "checkbox" ? (
        <input
          id={name}
          name={name}
          type="checkbox"
          checked={checked}
          onChange={(e) => onChange(e.target.checked ? "true" : "false")}
          className="mb-3 p-1 focus:outline-none focus:border focus:rounded"
        />
      ) : (
        <input
          id={name}
          name={name}
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="mb-3 p-1 border border-gray-400 rounded 
          focus:outline-none focus:border focus:border-black"
        />
      )}

      {error && <p className="text-red-500">{error}</p>}
    </>
  );
}

export default ValidatedInput;
