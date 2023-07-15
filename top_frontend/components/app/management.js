import { useEffect, useState } from "react";

export const Management = () => {
  const [jobs, setJobs] = useState([]);
  const [currentJob, setCurrentJob] = useState(null);
  const [jobTasks, setJobTasks] = useState([]);
  const [creatingJob, setCreatingJob] = useState(false);

  const getJobs = async () => {
    const res = await fetch("/api/theoneplugin/jobs");
    const data = await res.json();
    console.log("res: ", data);
    if (data?.jobs) {
      setJobs(data.jobs);
      setCurrentJob(data.jobs[0]?.job_name);
    }
  };

  const handleCreateJob = async ({ jobName, jobDescription }) => {
    if (!jobName || !jobDescription) {
      setCreatingJob(false);
      return;
    }
    const res = await fetch("/api/theoneplugin/jobs", {
      method: "POST",
      body: JSON.stringify({
        job_name: jobName,
        job_description: jobDescription,
      }),
    });
    const data = await res.json();
    console.log("res: ", data);
    if (data?.job) {
      setJobs([...jobs, data.job]);
      setCurrentJob(data.job.job_id);
    }
  };

  useEffect(() => {
    getJobs();
  }, []);

  return (
    <div className="flex flex-col w-full h-full bg-black text-white">
      <button
        className="bg-white text-black rounded px-3 py-1 w-[300px]"
        onClick={() => setCreatingJob(true)}
      >
        Create Job
      </button>
      {creatingJob && <CreateJobForm onClose={handleCreateJob} />}
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
          value={jobs.find((job) => job.job_id === currentJob)?.job_id}
          onChange={(e) => setCurrentJob(e.target.value)}
        >
          {jobs.map((job) => (
            <option
              key={job.job_id}
              value={job.job_id}
              selected={job.job_id === currentJob}
            >
              {job.job_name}
            </option>
          ))}
        </select>
      )}
    </div>
  );
};

const CreateJobForm = ({ onClose }) => {
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
