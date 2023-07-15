import { useEffect, useState } from "react";

export const Management = () => {
  const [jobs, setJobs] = useState([]);
  const [currentJob, setCurrentJob] = useState(null);
  const [jobTasks, setJobTasks] = useState([]);

  const getJobs = async () => {
    const res = await fetch("/api/theoneplugin/jobs");
    const data = await res.json();
    console.log("res: ", data);
    if (data?.jobs) {
      setJobs(data.jobs);
      setCurrentJob(data.jobs[0].id);
    }
  };

  useEffect(() => {
    getJobs();
  }, []);

  return (
    <div className="flex flex-col w-full h-full bg-black text-white">
      <button className="bg-white text-black rounded px-3 py-1">
        Create Job
      </button>
      <JobSelectionDropdown
        jobs={jobs}
        currentJob={currentJob}
        setCurrentJob={setCurrentJob}
      />
    </div>
  );
};

const JobSelectionDropdown = ({ jobs, currentJob, setCurrentJob }) => {
  return (
    <div className="flex flex-row">
      {!!jobs?.length && (
        <select
          value={jobs.find((job) => job.id === currentJob).id}
          onChange={(e) => setCurrentJob(e.target.value)}
        >
          {jobs.map((job) => (
            <option
              key={job.id}
              value={job.id}
              selected={job.id === currentJob}
            >
              {job.name}
            </option>
          ))}
        </select>
      )}
    </div>
  );
};
