import { useState } from "react";
export const CreateJobForm = ({ onClose }) => {
  const [jobName, setJobName] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  return (
    <div className="flex flex-col bg-white text-black p-4">
      <div className="flex flex-row">
        <div>Job Name</div>
        <input
          type="text"
          value={jobName}
          onChange={(e) => setJobName(e.target.value)}
          className="border-2 border-black rounded"
        />
      </div>
      <div className="flex flex-row">
        <div>Job Description</div>
        <textarea
          type="text"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          className="border-2 border-black rounded w-[500px]"
        />
      </div>
      <div className="flex flex-row">
        <button className="rounded px-3 py-1" onClick={onClose}>
          Cancel
        </button>
        <button
          className="rounded px-3 py-1"
          onClick={() => onClose({ jobName, jobDescription })}
        >
          Create
        </button>
      </div>
    </div>
  );
};
