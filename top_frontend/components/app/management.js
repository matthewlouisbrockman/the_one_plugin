import { useEffect, useState } from "react";
import { CreateJobForm } from "./ui/create_job_form";
import { JobSelectionDropdown } from "./ui/job_selection_dropdown";
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
