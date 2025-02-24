import React, { useState } from 'react';

interface SearchBarProps {
  onSearch: (city: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [input, setInput] = useState('');

  const handleSearch = () => {
    if (input.trim()) {
      onSearch(input);
    }
  };

  return (
    <div className="flex items-center">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Explore other cities!!"
        className="p-2 border border-gray-300 rounded-l"
      />
      <button
        onClick={handleSearch}
        className="p-2 bg-blue-500 text-white rounded-r"
      >
        Search
      </button>
    </div>
  );
};

export default SearchBar;