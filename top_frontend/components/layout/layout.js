import { NavBar } from "./navbar";

export const Layout = ({ children }) => {
  return (
    <div className="flex flex-col w-screen h-screen bg-black text-white">
      <NavBar />
      {children}
    </div>
  );
};
