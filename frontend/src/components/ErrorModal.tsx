import React from 'react';

interface ErrorModalProps {
  message: string;
  onClose: () => void;
}

const ErrorModal: React.FC<ErrorModalProps> = ({ message, onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-white bg-opacity-10 p-6 rounded-lg backdrop-blur-md">
        <p className="text-red-500">{message}</p>
        <button
          onClick={onClose}
          className="mt-4 p-2 bg-blue-500 rounded-lg"
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default ErrorModal;